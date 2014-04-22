quad\_to\_tri.py
================
A simple, no-dependencies script for turning .obj files that encode quad
meshes into .obj files of equivalent tri meshes, accomplished by just
splitting the quads along the diagonal into two triangles.

This script **cannot** be used to convert tri meshes into quad meshes, a
significantly harder problem.

Caveats
-------
Any comments, material specifications, or other .obj features which are not
vertices, texture coordinates, normals, or faces will *not* be preserved in
the output.

Usage
-----
```
./quad_to_tri.py [source file] [destination file]
```
will turn a quad mesh at `[source file]` into a destination mesh at
`[destination file]`.
```
./quad_to_tri.py [source file]
```
will turn a quad mesh at `[source file]` into a tri mesh and print to standard
output.
