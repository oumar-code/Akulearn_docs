export default MediaKitPanel;
"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";
import styles from "./media-kit.module.css";

  type Asset = { id: string; url: string; name: string };
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploadMsg, setUploadMsg] = useState("");

  useEffect(() => {
    const fetchAssets = async () => {
      setLoading(true);
      setError("");
      try {
        // Replace 'media_kit' with your actual table or storage bucket logic
        const { data, error } = await supabase.from('media_kit').select('*');
        if (error) throw error;
        setAssets(data || []);
      } catch (err) {
        setError("Unable to fetch media kit assets. Please check your Supabase table or storage.");
      }
      setLoading(false);
    };
    fetchAssets();
  }, []);

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) return;
    setUploadMsg('Uploading...');
    // Example: upload to Supabase Storage bucket 'media-kit'
    const { data, error } = await supabase.storage.from('media-kit').upload(file.name, file);
    if (error) setUploadMsg(error.message);
    else setUploadMsg('Upload successful!');
  };

  return (
    <div className={styles.mediaPanel}>
      <h3>Media Kit</h3>
      {loading && <div>Loading assets...</div>}
      {error && <div className={styles.mediaError}>{error}</div>}
      <ul className={styles.mediaList}>
        {assets.map(asset => (
          <li key={asset.id}>
            <a href={asset.url} target="_blank" rel="noopener noreferrer">{asset.name}</a>
          </li>
        ))}
      </ul>
      <form onSubmit={handleUpload} className={styles.mediaForm}>
        <input type="file" onChange={e => {
          if (e.target.files && e.target.files[0]) setFile(e.target.files[0]);
        }} />
        <button type="submit">Upload</button>
      </form>
      <div>{uploadMsg}</div>
    </div>
  );
}
