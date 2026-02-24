import os
import glob
import gpxpy
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import contextily as ctx
import osmnx as ox

# =========================
# 1. LOAD GPX FILES
# =========================

gpx_folder = "data_raw/strava_runs"
gpx_files = glob.glob(os.path.join(gpx_folder, "*.gpx"))

lines = []

for file in gpx_files:
    with open(file, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

        for track in gpx.tracks:
            for segment in track.segments:
                points = [(point.longitude, point.latitude) for point in segment.points]
                if len(points) > 1:
                    lines.append(LineString(points))

if len(lines) == 0:
    raise ValueError("Tidak ada data GPX ditemukan.")

gdf = gpd.GeoDataFrame(geometry=lines, crs="EPSG:4326")

# =========================
# 2. PROJECT TO WEB MERCATOR
# =========================

gdf = gdf.to_crs(epsg=3857)

# =========================
# 3. AMBIL BATAS WILAYAH DARI OSM
# =========================

place_name = "Jakarta, Indonesia"

boundary = ox.geocode_to_gdf(place_name)
boundary = boundary.to_crs(epsg=3857)

# =========================
# 4. CLIP DATA
# =========================

gdf_clipped = gpd.clip(gdf, boundary)

# =========================
# 5. PLOT
# =========================

fig, ax = plt.subplots(figsize=(10, 10))

# Plot heat effect (overlay banyak garis)
gdf_clipped.plot(
    ax=ax,
    linewidth=6,
    alpha=0.08,
    color="#F95418"
)
gdf_clipped.plot(
    ax=ax,
    linewidth=1.2,
    alpha=0.6,
    color="#FC4C02"
)

# Basemap
ctx.add_basemap(
    ax,
    source=ctx.providers.CartoDB.DarkMatter
)

# Crop ke boundary
minx, miny, maxx, maxy = gdf_clipped.total_bounds
buffer = 300  # meter (bisa kamu ubah)

ax.set_xlim(minx - buffer, maxx + buffer)
ax.set_ylim(miny - buffer, maxy + buffer)

ax.set_axis_off()

# =========================
# 6. SAVE OUTPUT
# =========================

os.makedirs("output_maps", exist_ok=True)

output_path = "output_maps/day02_strava_heatmap.png"
plt.savefig(output_path, dpi=400, bbox_inches="tight")
plt.close()

print(f"Heatmap berhasil dibuat dan disimpan di: {output_path}")