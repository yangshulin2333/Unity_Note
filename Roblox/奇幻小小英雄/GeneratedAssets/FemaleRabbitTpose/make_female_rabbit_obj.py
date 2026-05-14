import math
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
OBJ_PATH = OUT_DIR / "female_rabbit_tpose_lowpoly.obj"
MTL_PATH = OUT_DIR / "female_rabbit_tpose_lowpoly.mtl"


class MeshBuilder:
    def __init__(self):
        self.vertices = []
        self.faces = []

    def add_vertex(self, p):
        self.vertices.append(p)
        return len(self.vertices)

    def add_face(self, material, indices):
        self.faces.append((material, indices))


def rot_z(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return ((c, -s, 0.0), (s, c, 0.0), (0.0, 0.0, 1.0))


def apply_rot(rot, p):
    if rot is None:
        return p
    x, y, z = p
    return (
        rot[0][0] * x + rot[0][1] * y + rot[0][2] * z,
        rot[1][0] * x + rot[1][1] * y + rot[1][2] * z,
        rot[2][0] * x + rot[2][1] * y + rot[2][2] * z,
    )


def add_ellipsoid(mesh, name, center, scale, material, segments=20, rings=10, rot=None):
    cx, cy, cz = center
    sx, sy, sz = scale
    rows = []
    for r in range(rings + 1):
        theta = math.pi * r / rings
        row = []
        for s in range(segments):
            phi = 2.0 * math.pi * s / segments
            local = (
                sx * math.sin(theta) * math.cos(phi),
                sy * math.cos(theta),
                sz * math.sin(theta) * math.sin(phi),
            )
            rx, ry, rz = apply_rot(rot, local)
            row.append(mesh.add_vertex((cx + rx, cy + ry, cz + rz)))
        rows.append(row)

    for r in range(rings):
        for s in range(segments):
            a = rows[r][s]
            b = rows[r][(s + 1) % segments]
            c = rows[r + 1][(s + 1) % segments]
            d = rows[r + 1][s]
            mesh.add_face(material, [a, b, c, d])


def add_cylinder_x(mesh, name, center, length, radius_y, radius_z, material, segments=16):
    cx, cy, cz = center
    x0 = cx - length / 2
    x1 = cx + length / 2
    left = []
    right = []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments
        y = math.cos(a) * radius_y
        z = math.sin(a) * radius_z
        left.append(mesh.add_vertex((x0, cy + y, cz + z)))
        right.append(mesh.add_vertex((x1, cy + y, cz + z)))
    for i in range(segments):
        mesh.add_face(material, [left[i], left[(i + 1) % segments], right[(i + 1) % segments], right[i]])
    mesh.add_face(material, list(reversed(left)))
    mesh.add_face(material, right)


def add_cylinder_y(mesh, name, center, height, radius_x, radius_z, material, segments=16):
    cx, cy, cz = center
    y0 = cy - height / 2
    y1 = cy + height / 2
    bottom = []
    top = []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments
        x = math.cos(a) * radius_x
        z = math.sin(a) * radius_z
        bottom.append(mesh.add_vertex((cx + x, y0, cz + z)))
        top.append(mesh.add_vertex((cx + x, y1, cz + z)))
    for i in range(segments):
        mesh.add_face(material, [bottom[i], bottom[(i + 1) % segments], top[(i + 1) % segments], top[i]])
    mesh.add_face(material, list(reversed(bottom)))
    mesh.add_face(material, top)


def add_frustum_y(mesh, name, center, height, top_rx, top_rz, bottom_rx, bottom_rz, material, segments=20):
    cx, cy, cz = center
    y0 = cy - height / 2
    y1 = cy + height / 2
    bottom = []
    top = []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments
        bottom.append(mesh.add_vertex((cx + math.cos(a) * bottom_rx, y0, cz + math.sin(a) * bottom_rz)))
        top.append(mesh.add_vertex((cx + math.cos(a) * top_rx, y1, cz + math.sin(a) * top_rz)))
    for i in range(segments):
        mesh.add_face(material, [bottom[i], bottom[(i + 1) % segments], top[(i + 1) % segments], top[i]])
    mesh.add_face(material, list(reversed(bottom)))
    mesh.add_face(material, top)


def add_box(mesh, name, center, size, material):
    cx, cy, cz = center
    sx, sy, sz = [v / 2 for v in size]
    verts = [
        (cx - sx, cy - sy, cz - sz),
        (cx + sx, cy - sy, cz - sz),
        (cx + sx, cy + sy, cz - sz),
        (cx - sx, cy + sy, cz - sz),
        (cx - sx, cy - sy, cz + sz),
        (cx + sx, cy - sy, cz + sz),
        (cx + sx, cy + sy, cz + sz),
        (cx - sx, cy + sy, cz + sz),
    ]
    ids = [mesh.add_vertex(v) for v in verts]
    for face in ([0, 1, 2, 3], [5, 4, 7, 6], [4, 0, 3, 7], [1, 5, 6, 2], [3, 2, 6, 7], [4, 5, 1, 0]):
        mesh.add_face(material, [ids[i] for i in face])


def write_mtl():
    materials = {
        "fur_white": (0.93, 0.86, 0.78),
        "fur_cream": (1.0, 0.91, 0.78),
        "ear_pink": (1.0, 0.47, 0.55),
        "outfit_pink": (0.92, 0.38, 0.45),
        "outfit_cream": (0.98, 0.85, 0.63),
        "leather": (0.42, 0.21, 0.10),
        "gold": (1.0, 0.68, 0.18),
        "eye_dark": (0.08, 0.03, 0.05),
        "eye_pink": (0.95, 0.30, 0.42),
        "nose": (1.0, 0.30, 0.42),
    }
    with MTL_PATH.open("w", encoding="utf-8") as f:
        for name, color in materials.items():
            r, g, b = color
            f.write(f"newmtl {name}\n")
            f.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
            f.write("Ka 0.0500 0.0500 0.0500\n")
            f.write("Ks 0.1200 0.1200 0.1200\n")
            f.write("Ns 20\n\n")


def build_model():
    mesh = MeshBuilder()

    # Body and head proportions are intentionally simple for easy Roblox import.
    add_ellipsoid(mesh, "torso", (0, 1.45, 0), (0.32, 0.48, 0.22), "outfit_cream", 20, 10)
    add_frustum_y(mesh, "pink_tunic", (0, 1.20, 0), 0.35, 0.32, 0.22, 0.48, 0.30, "outfit_pink", 20)
    add_cylinder_y(mesh, "belt", (0, 1.36, -0.01), 0.075, 0.39, 0.255, "leather", 20)
    add_box(mesh, "belt_buckle", (0.18, 1.36, -0.255), (0.09, 0.07, 0.025), "gold")

    add_ellipsoid(mesh, "head", (0, 2.25, -0.02), (0.34, 0.32, 0.30), "fur_white", 24, 12)
    add_ellipsoid(mesh, "muzzle", (0, 2.13, -0.31), (0.16, 0.09, 0.07), "fur_cream", 18, 8)
    add_ellipsoid(mesh, "nose", (0, 2.17, -0.385), (0.045, 0.028, 0.018), "nose", 12, 6)
    add_ellipsoid(mesh, "left_eye", (-0.13, 2.27, -0.295), (0.055, 0.08, 0.015), "eye_pink", 12, 6)
    add_ellipsoid(mesh, "right_eye", (0.13, 2.27, -0.295), (0.055, 0.08, 0.015), "eye_pink", 12, 6)
    add_ellipsoid(mesh, "left_pupil", (-0.13, 2.27, -0.312), (0.025, 0.045, 0.008), "eye_dark", 10, 5)
    add_ellipsoid(mesh, "right_pupil", (0.13, 2.27, -0.312), (0.025, 0.045, 0.008), "eye_dark", 10, 5)

    add_ellipsoid(mesh, "left_ear", (-0.19, 2.82, 0.0), (0.10, 0.55, 0.045), "fur_white", 16, 8, rot_z(0.14))
    add_ellipsoid(mesh, "right_ear", (0.19, 2.82, 0.0), (0.10, 0.55, 0.045), "fur_white", 16, 8, rot_z(-0.14))
    add_ellipsoid(mesh, "left_inner_ear", (-0.19, 2.82, -0.045), (0.055, 0.43, 0.018), "ear_pink", 12, 6, rot_z(0.14))
    add_ellipsoid(mesh, "right_inner_ear", (0.19, 2.82, -0.045), (0.055, 0.43, 0.018), "ear_pink", 12, 6, rot_z(-0.14))

    # T-pose arms.
    add_cylinder_x(mesh, "left_upper_arm", (-0.55, 1.72, 0), 0.46, 0.075, 0.07, "fur_white", 16)
    add_cylinder_x(mesh, "left_forearm", (-1.02, 1.72, 0), 0.48, 0.065, 0.06, "fur_white", 16)
    add_cylinder_x(mesh, "right_upper_arm", (0.55, 1.72, 0), 0.46, 0.075, 0.07, "fur_white", 16)
    add_cylinder_x(mesh, "right_forearm", (1.02, 1.72, 0), 0.48, 0.065, 0.06, "fur_white", 16)
    add_cylinder_x(mesh, "left_glove", (-1.31, 1.72, 0), 0.22, 0.075, 0.06, "leather", 14)
    add_cylinder_x(mesh, "right_glove", (1.31, 1.72, 0), 0.22, 0.075, 0.06, "leather", 14)

    # Legs and boots.
    add_cylinder_y(mesh, "left_leg", (-0.16, 0.72, 0), 0.88, 0.095, 0.075, "fur_white", 16)
    add_cylinder_y(mesh, "right_leg", (0.16, 0.72, 0), 0.88, 0.095, 0.075, "fur_white", 16)
    add_cylinder_y(mesh, "left_boot", (-0.16, 0.22, -0.02), 0.35, 0.12, 0.10, "leather", 16)
    add_cylinder_y(mesh, "right_boot", (0.16, 0.22, -0.02), 0.35, 0.12, 0.10, "leather", 16)
    add_box(mesh, "left_foot", (-0.16, 0.03, -0.08), (0.22, 0.09, 0.28), "leather")
    add_box(mesh, "right_foot", (0.16, 0.03, -0.08), (0.22, 0.09, 0.28), "leather")

    add_ellipsoid(mesh, "tail", (0.0, 1.08, 0.27), (0.14, 0.12, 0.12), "fur_white", 14, 7)

    return mesh


def write_obj(mesh):
    with OBJ_PATH.open("w", encoding="utf-8") as f:
        f.write("# Low-poly female rabbit T-pose reference generated from 2D concept.\n")
        f.write(f"mtllib {MTL_PATH.name}\n")
        for x, y, z in mesh.vertices:
            f.write(f"v {x:.5f} {y:.5f} {z:.5f}\n")
        current = None
        for material, indices in mesh.faces:
            if material != current:
                f.write(f"usemtl {material}\n")
                current = material
            f.write("f " + " ".join(str(i) for i in indices) + "\n")


def main():
    write_mtl()
    mesh = build_model()
    write_obj(mesh)
    print(f"Wrote {OBJ_PATH}")
    print(f"Wrote {MTL_PATH}")
    print(f"Vertices: {len(mesh.vertices)} Faces: {len(mesh.faces)}")


if __name__ == "__main__":
    main()
