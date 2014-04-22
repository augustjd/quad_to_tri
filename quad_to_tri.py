#!/usr/bin/env python

from collections import namedtuple
import operator
import sys

FaceVertex = namedtuple('FaceVertex', ('vertex', 'texture_coord', 'normal'))

class Face:
    def __init__(self, vertices):
        self.vertices = vertices

    def __str__(self):
        def face_vertex_to_string(face_vertex):
            return "{0}/{1}/{2}".format(
                    face_vertex.vertex, 
                    face_vertex.texture_coord,
                    face_vertex.normal)

        return "f {0}".format(" ".join(map(face_vertex_to_string, self.vertices)))

    def to_tri(self):
        """If this face is triangular, returns an array of a copy of this
        face.  If this face is a quad, returns an array of two triangles which
        are equivalent to this face."""

        if len(self.vertices) == 3:
            return [Face(self.vertices)]
        if len(self.vertices) == 4:
            return [Face([self.vertices[0], self.vertices[1], self.vertices[2]]), 
                    Face([self.vertices[0], self.vertices[2], self.vertices[3]])]

    def to_obj_line(self):
        return str(self)

    def from_obj_line(line):
        if not line.startswith('f '):
            raise ValueError("""Failed parsing Face from .obj line - it didn't
                begin with 'f'""")
        face_vertices = []
        splits = line.split(" ")
        for split in splits[1:]: # skip f 
            face_vertices.append(FaceVertex(*map(int, split.split("/"))))

        return Face(face_vertices)

    from_obj_line = staticmethod(from_obj_line)

class Mesh:
    def __init__(self, vertices, texture_coords, normals, faces):
        self.vertices       = vertices
        self.texture_coords = texture_coords
        self.normals        = normals
        self.faces          = faces

    def vertex_from_string(line):
        return map(float, line.split(' ')[1:])
    vertex_from_string = staticmethod(vertex_from_string)

    def vertex_to_string(vertex):
        return "v {0} {1} {2}".format(*vertex)
    vertex_to_string = staticmethod(vertex_to_string)

    def vertex_normal_to_string(normal):
        return "vn {0} {1} {2}".format(*normal)
    vertex_normal_to_string = staticmethod(vertex_normal_to_string)

    def vertex_texture_coord_to_string(texture_coord):
        return "vt {0} {1}".format(*texture_coord)
    vertex_texture_coord_to_string = staticmethod(vertex_texture_coord_to_string)

    def to_tri(self):
        return Mesh(self.vertices, 
                self.texture_coords, 
                self.normals,
                reduce(operator.add, map(Face.to_tri, self.faces)))

    def to_obj(self):
        return "\n".join([
            "\n".join(map(Mesh.vertex_to_string, self.vertices)),
            "\n".join(map(Mesh.vertex_normal_to_string, self.normals)),
            "\n".join(map(Mesh.vertex_texture_coord_to_string, self.texture_coords)),
            "\n".join(map(Face.to_obj_line, self.faces))
        ])

    def from_obj(text):
        vertices = []
        texture_coords = []
        normals = []
        faces = []

        for line in text.split('\n'):
            if line.startswith('v '):
                vertices.append(Mesh.vertex_from_string(line))
            if line.startswith('vt '):
                texture_coords.append(Mesh.vertex_from_string(line))
            if line.startswith('vn '):
                normals.append(Mesh.vertex_from_string(line))
            if line.startswith('f '):
                faces.append(Face.from_obj_line(line))

            # otherwise, ignore the line silently for now.

        return Mesh(vertices, texture_coords, normals, faces)
    from_obj = staticmethod(from_obj)

    def from_obj_file(f):
        return Mesh.from_obj(f.read())
    from_obj_file = staticmethod(from_obj_file)

if __name__ == "__main__":
    try:
        mesh_file   = open(sys.argv[1])
    except Exception:
        print "Failed to load", sys.argv[1]
        exit(0)

    if len(sys.argv) == 3:
        try:
            sys.stdout = open(sys.argv[2], 'w')
        except Exception:
            print "Failed to open", sys.argv[2], "for output."
            exit(0)

    mesh = Mesh.from_obj_file(mesh_file)
    trimesh = mesh.to_tri()

    sys.stdout.write(trimesh.to_obj())
    sys.stdout.flush()
    sys.stdout.close()
