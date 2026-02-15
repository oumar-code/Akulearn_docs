"""
Chemistry Models Generator
Generates 3D molecular structures and chemical diagrams
- Molecule visualization from SMILES notation
- 2D and 3D representations
- Molecular properties calculation
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import numpy as np

# Optional imports - will fail gracefully if not available
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw, Descriptors
    from rdkit.Chem import rdMolDescriptors
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("RDKit not available. Chemistry models generator will use fallback mode.")

logger = logging.getLogger(__name__)


class ChemistryModelGenerator:
    """Generate 3D molecular structures for chemistry lessons"""
    
    def __init__(self, output_dir="generated_assets/molecules"):
        """
        Initialize chemistry model generator
        
        Args:
            output_dir: Directory to save generated molecules
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rdkit_available = RDKIT_AVAILABLE
        
        if not self.rdkit_available:
            logger.warning("⚠️ RDKit not available. Using fallback mode.")
        
        logger.info(f"ChemistryModelGenerator initialized: {self.output_dir}")
    
    def generate_molecule_3d(self, smiles: str, name: str) -> Dict[str, Any]:
        """
        Generate 3D model from SMILES notation
        
        Args:
            smiles: SMILES notation of the molecule
            name: Name of the molecule
            
        Returns:
            Dictionary with metadata and file paths
        """
        if not self.rdkit_available:
            logger.warning(f"⚠️ Skipping RDKit generation for {name} - RDKit not available")
            return self._generate_fallback_metadata(smiles, name)
        
        try:
            # Create molecule from SMILES
            mol = Chem.MolFromSmiles(smiles)
            
            if mol is None:
                raise ValueError(f"Invalid SMILES: {smiles}")
            
            # Add hydrogens and generate 3D coordinates
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol)
            
            # Export to MOL format
            mol_block = Chem.MolToMolBlock(mol)
            
            # Save MOL file
            mol_path = self.output_dir / f"{name}.mol"
            with open(mol_path, 'w') as f:
                f.write(mol_block)
            
            # Generate 2D structure image
            img = Draw.MolToImage(mol, size=(400, 400))
            img_path = self.output_dir / f"{name}_2d.png"
            img.save(img_path)
            
            # Remove hydrogens for cleaner 2D image
            mol_no_h = Chem.RemoveHs(mol)
            img_no_h = Draw.MolToImage(mol_no_h, size=(400, 400))
            img_no_h_path = self.output_dir / f"{name}_2d_clean.png"
            img_no_h.save(img_no_h_path)
            
            # Create metadata
            metadata = {
                "name": name,
                "smiles": smiles,
                "mol_file": str(mol_path),
                "image_2d": str(img_path),
                "image_2d_clean": str(img_no_h_path),
                "formula": rdMolDescriptors.CalcMolFormula(mol),
                "molecular_weight": float(rdMolDescriptors.CalcExactMolWt(mol)),
                "num_atoms": int(mol.GetNumAtoms()),
                "num_bonds": int(mol.GetNumBonds()),
                "logp": float(Descriptors.MolLogP(mol)),
                "hbd": int(Descriptors.NumHDonors(mol)),
                "hba": int(Descriptors.NumHAcceptors(mol)),
                "rotatable_bonds": int(Descriptors.NumRotatableBonds(mol))
            }
            
            metadata_path = self.output_dir / f"{name}_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"✅ Generated molecule: {name}")
            return metadata
            
        except Exception as e:
            logger.error(f"❌ Failed to generate molecule {name}: {e}")
            raise
    
    def _generate_fallback_metadata(self, smiles: str, name: str) -> Dict[str, Any]:
        """Generate basic metadata without RDKit"""
        return {
            "name": name,
            "smiles": smiles,
            "status": "fallback_mode",
            "note": "Generated without RDKit - install rdkit-pypi for full features"
        }
    
    def generate_hydrocarbons(self) -> List[Dict[str, Any]]:
        """Generate common hydrocarbon molecules"""
        hydrocarbons = [
            ("C", "methane", "CH₄"),
            ("CC", "ethane", "C₂H₆"),
            ("CCC", "propane", "C₃H₈"),
            ("CCCC", "butane", "C₄H₁₀"),
            ("C=C", "ethene", "C₂H₄"),
            ("C=CC", "propene", "C₃H₆"),
            ("C#C", "ethyne", "C₂H₂"),
            ("c1ccccc1", "benzene", "C₆H₆"),
        ]
        
        generated = []
        logger.info("⚗️ Generating hydrocarbons...")
        
        for smiles, name, formula in hydrocarbons:
            try:
                metadata = self.generate_molecule_3d(smiles, name)
                generated.append(metadata)
            except Exception as e:
                logger.warning(f"⚠️ Failed {name}: {e}")
        
        return generated
    
    def generate_common_molecules(self) -> List[Dict[str, Any]]:
        """Generate common molecules for chemistry lessons"""
        molecules = [
            ("O", "water", "H₂O"),
            ("O=C=O", "carbon_dioxide", "CO₂"),
            ("[O-][N+](=O)c1ccccc1", "nitrobenzene", "C₆H₅NO₂"),
            ("CC(=O)O", "acetic_acid", "C₂H₄O₂"),
            ("C(C(=O)O)N", "glycine", "C₂H₅NO₂"),
            ("c1ccc(cc1)O", "phenol", "C₆H₆O"),
            ("CC(C)CC(NC(=O)C(CC(=O)N)NC(=O)C(CC(C)C)NC(=O)C(CC(=O)O)NC(=O)C(CC(C)C)NC(=O)C(CC(C)C)NC(=O)C(Cc1ccc(O)cc1)NC(=O)C(Cc1c[nH]cn1)NC(=O)C(Cc1ccccc1)NC(=O)CNC(=O)C)C(=O)NCC(=O)N", "protein", "Complex"),
        ]
        
        generated = []
        logger.info("🧬 Generating common molecules...")
        
        for smiles, name, formula in molecules:
            try:
                metadata = self.generate_molecule_3d(smiles, name)
                generated.append(metadata)
            except Exception as e:
                logger.warning(f"⚠️ Failed {name}: {e}")
        
        return generated
    
    def generate_inorganic_molecules(self) -> List[Dict[str, Any]]:
        """Generate inorganic molecules"""
        inorganic = [
            ("N#N", "nitrogen", "N₂"),
            ("O=O", "oxygen", "O₂"),
            ("[Na+].[Cl-]", "sodium_chloride", "NaCl"),
            ("Cl[Si](Cl)(Cl)Cl", "silicon_tetrachloride", "SiCl₄"),
        ]
        
        generated = []
        logger.info("⚛️ Generating inorganic molecules...")
        
        for smiles, name, formula in inorganic:
            try:
                metadata = self.generate_molecule_3d(smiles, name)
                generated.append(metadata)
            except Exception as e:
                logger.warning(f"⚠️ Failed {name}: {e}")
        
        return generated
    
    def generate_all_priority_molecules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate all priority molecules for curriculum"""
        results = {
            "hydrocarbons": [],
            "common_molecules": [],
            "inorganic_molecules": []
        }
        
        results["hydrocarbons"] = self.generate_hydrocarbons()
        results["common_molecules"] = self.generate_common_molecules()
        results["inorganic_molecules"] = self.generate_inorganic_molecules()
        
        return results
    
    def generate_manifest(self, molecules: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate manifest file with all molecule metadata"""
        try:
            total = sum(len(v) for v in molecules.values())
            manifest = {
                "generated_at": str(np.datetime64('today')),
                "total_molecules": total,
                "categories": molecules
            }
            
            manifest_path = self.output_dir / "molecules_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info(f"✅ Generated manifest: {manifest_path}")
            return str(manifest_path)
        except Exception as e:
            logger.error(f"❌ Error generating manifest: {e}")
            raise


if __name__ == "__main__":
    # Test basic generation
    logging.basicConfig(level=logging.INFO)
    
    if not RDKIT_AVAILABLE:
        print("⚠️ RDKit not available. Install with: pip install rdkit-pypi")
        print("Skipping chemistry tests.")
    else:
        generator = ChemistryModelGenerator()
        
        print("\n" + "="*50)
        print("⚗️ Chemistry Molecules Generated:")
        print("="*50)
        
        molecules = generator.generate_all_priority_molecules()
        for category, items in molecules.items():
            print(f"\n{category.upper()}:")
            for item in items:
                print(f"  ✅ {item['name']}")
        
        # Generate manifest
        generator.generate_manifest(molecules)
