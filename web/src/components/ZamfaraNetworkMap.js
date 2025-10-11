import React, { useState, useEffect, useMemo } from 'react';
import Map, { Source, Layer, Popup } from 'react-map-gl';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_ACCESS_TOKEN || 'YOUR_MAPBOX_ACCESS_TOKEN';

const ZamfaraNetworkMap = () => {
  const [viewport, setViewport] = useState({
    latitude: 12.16,
    longitude: 6.37,
    zoom: 7,
    bearing: 0,
    pitch: 0,
  });
  const [data, setData] = useState(null);
  const [popupInfo, setPopupInfo] = useState(null);
  const [showT1, setShowT1] = useState(true);
  const [showT2, setShowT2] = useState(true);
  const [showT3, setShowT3] = useState(true);

  // Example API integration: fetch metrics from backend
  const [edgeMetrics, setEdgeMetrics] = useState(null);
  useEffect(() => {
    fetch('http://localhost:8081/metrics/edge')
      .then(res => res.json())
      .then(setEdgeMetrics)
      .catch(() => setEdgeMetrics(null));
  }, []);

  useEffect(() => {
    fetch('/data/zamfara-network-data.geojson')
      .then(res => res.json())
      .then(setData)
      .catch(error => console.error("Error loading GeoJSON data:", error));
  }, []);

  const networkData = useMemo(() => {
    if (!data) return { hubs: { type: "FeatureCollection", features: [] }, links: { type: "FeatureCollection", features: [] } };
    const hubs = { type: "FeatureCollection", features: data.features.filter(f => f.geometry.type === 'Point') };
    const links = { type: "FeatureCollection", features: data.features.filter(f => f.geometry.type === 'LineString') };
    return { hubs, links };
  }, [data]);

  const TIER_COLORS = {
    T1_EDGE_HUB: '#00FF00',
    T2_SUPER_HUB: '#FFA500',
    T3_IG_HUB: '#800080',
  };

  const hubLayerStyle = {
    id: 'hubs',
    type: 'circle',
    source: 'hubs-data',
    paint: {
      'circle-color': [
        'match',
        ['get', 'tier'],
        'T3_IG_HUB', TIER_COLORS.T3_IG_HUB,
        'T2_SUPER_HUB', TIER_COLORS.T2_SUPER_HUB,
        TIER_COLORS.T1_EDGE_HUB
      ],
      'circle-radius': [
        'match',
        ['get', 'tier'],
        'T3_IG_HUB', 15,
        'T2_SUPER_HUB', 10,
        5
      ],
      'circle-stroke-width': 1.5,
      'circle-stroke-color': '#FFFFFF'
    }
  };

  const linkLayerStyle = {
    id: 'links',
    type: 'line',
    source: 'links-data',
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: {
      'line-color': [
        'match',
        ['get', 'tier_link'],
        'T2-T3', TIER_COLORS.T3_IG_HUB,
        'T2-T2', TIER_COLORS.T2_SUPER_HUB,
        TIER_COLORS.T1_EDGE_HUB
      ],
      'line-width': [
        'match',
        ['get', 'tier_link'],
        'T2-T3', 4,
        'T2-T2', 3,
        2
      ]
    }
  };

  const onClick = (event) => {
    const feature = event.features && event.features[0];
    if (feature && feature.layer.id === 'hubs') {
      const [longitude, latitude] = feature.geometry.coordinates;
      setPopupInfo({
        longitude,
        latitude,
        properties: feature.properties,
      });
    } else {
      setPopupInfo(null);
    }
  };

  return (
    <div style={{ height: '80vh', width: '100%' }}>
      {/* Layer toggles */}
      <div style={{ marginBottom: '10px' }}>
        <label><input type="checkbox" checked={showT1} onChange={e => setShowT1(e.target.checked)} /> Tier 1 Edge Hubs</label>
        <label style={{ marginLeft: '10px' }}><input type="checkbox" checked={showT2} onChange={e => setShowT2(e.target.checked)} /> Tier 2 Super Hubs</label>
        <label style={{ marginLeft: '10px' }}><input type="checkbox" checked={showT3} onChange={e => setShowT3(e.target.checked)} /> Tier 3 IG-Hub</label>
      </div>
      {/* Legend */}
      <div style={{ marginBottom: '10px', background: '#fff', padding: '5px', borderRadius: '5px', display: 'inline-block' }}>
        <span style={{ color: '#00FF00', fontWeight: 'bold' }}>●</span> Tier 1 Edge Hub
        <span style={{ color: '#FFA500', fontWeight: 'bold', marginLeft: '10px' }}>●</span> Tier 2 Super Hub
        <span style={{ color: '#800080', fontWeight: 'bold', marginLeft: '10px' }}>●</span> Tier 3 IG-Hub
      </div>
      {/* Metrics Example */}
      {edgeMetrics && (
        <div style={{ marginBottom: '10px', background: '#e6f7ff', padding: '5px', borderRadius: '5px', display: 'inline-block' }}>
          <strong>Edge Metrics:</strong> DC/NP Ratio: {edgeMetrics.dc_np_ratio}
        </div>
      )}
      <Map
        {...viewport}
        mapboxAccessToken={MAPBOX_TOKEN}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/light-v11"
        onMove={evt => setViewport(evt.viewState)}
        interactiveLayerIds={['hubs']}
        onClick={onClick}
      >
        <Source id="links-data" type="geojson" data={networkData.links}>
          <Layer {...linkLayerStyle} />
        </Source>
        <Source id="hubs-data" type="geojson" data={networkData.hubs}>
          <Layer {...hubLayerStyle} />
        </Source>
        {popupInfo && (
          <Popup
            longitude={popupInfo.longitude}
            latitude={popupInfo.latitude}
            onClose={() => setPopupInfo(null)}
            closeButton={true}
            closeOnClick={false}
            anchor="bottom"
          >
            <div style={{ padding: '5px', maxWidth: '200px' }}>
              <h4 style={{ color: TIER_COLORS[popupInfo.properties.tier], margin: '0 0 5px 0' }}>
                {popupInfo.properties.name}
              </h4>
              <p><strong>Tier:</strong> {popupInfo.properties.tier.replace('_', ' ')}</p>
              <p><strong>LGA:</strong> {popupInfo.properties.connected_lga || 'N/A'}</p>
              <p><strong>Capacity:</strong> {popupInfo.properties.capacity_gbps} Gbps</p>
              <p><strong>Status:</strong> {popupInfo.properties.status}</p>
            </div>
          </Popup>
        )}
      </Map>
    </div>
  );
};

export default ZamfaraNetworkMap;
