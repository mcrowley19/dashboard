/**
 * Blender asset for landing hero.
 * asset_base_id: d1bfff0f-a4bb-4fa1-981e-9812a4c2380a
 * asset_type: model
 *
 * Place your exported GLB at public/models/d1bfff0f-a4bb-4fa1-981e-9812a4c2380a.glb
 * or set VITE_ASSET_BASE_URL (e.g. https://your-cdn.com) to load from an API/CDN.
 */
const ASSET_ID = 'd1bfff0f-a4bb-4fa1-981e-9812a4c2380a'

export const LANDING_ASSET = {
  asset_base_id: ASSET_ID,
  asset_type: 'model' as const,
  /** Resolved model URL: from env or /models/{id}.glb in public */
  get modelUrl(): string {
    const base = import.meta.env.VITE_ASSET_BASE_URL
    return base ? `${base.replace(/\/$/, '')}/models/${ASSET_ID}.glb` : `/models/${ASSET_ID}.glb`
  },
}
