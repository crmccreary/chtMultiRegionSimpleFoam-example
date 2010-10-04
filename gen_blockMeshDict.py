import os

class Point(object):
    next_id = 0
    def __init__(self, 
                 x, 
                 y, 
                 z):
        self.id = Point.next_id
        Point.next_id = Point.next_id + 1
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def __cmp__(self, other):
        if self.id < other.id:
            return -1
        elif self.id == other.id:
            return 0
        else:
            return 1

    def translate(self, x=0, y=0, z=0):
        return Point(self.x + x,
                     self.y + y,
                     self.z + z)

    def __str__(self):
        # Convert to meters
        return "    (%s %s %s) // Vertex %s" % (self.x/1000.0, self.y/1000.0, self.z/1000.0, self.id)

class Face(object):
    def __init__(self, conn):
        self.connectivity = conn

    def __str__(self):
        conn = ''.join([str(vrt) + ' '  for vrt in self.connectivity])
        return "        (%s)" % (conn,)

class Patch(object):
    def __init__(self, type, name, faces):
        self.type = type
        self.name = name
        self.faces = faces

    def __str__(self):
        s = "    %s %s\n" % (self.type, self.name)
        s = s + "    (\n"
        for face in self.faces:
            s = s + "%s\n" % (face,)
        s = s + "    )\n"
        return s

class Cell(object):
    def __init__(self, 
                 connectivity, 
                 nx, 
                 ny, 
                 nz, 
                 grad_x = 1, 
                 grad_y = 1, 
                 grad_z = 1):
        self.id = id
        self.connectivity = connectivity
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.grad_x = grad_x
        self.grad_y = grad_y
        self.grad_z = grad_z
        self.f0 = Face([connectivity[0],
                        connectivity[3],
                        connectivity[2],
                        connectivity[1]])
        self.f1 = Face([connectivity[4],
                        connectivity[5],
                        connectivity[6],
                        connectivity[7]])
        self.f2 = Face([connectivity[0],
                        connectivity[1],
                        connectivity[5],
                        connectivity[4]])
        self.f3 = Face([connectivity[1],
                        connectivity[2],
                        connectivity[6],
                        connectivity[5]])
        self.f4 = Face([connectivity[2],
                        connectivity[3],
                        connectivity[7],
                        connectivity[6]])
        self.f5 = Face([connectivity[0],
                        connectivity[4],
                        connectivity[7],
                        connectivity[3]])

    def __cmp__(self, other):
        if self.id < other.id:
            return -1
        elif self.id == other.id:
            return 0
        else:
            return 1

    def __str__(self):
        conn = ''.join([str(vrt) + ' '  for vrt in self.connectivity])
        return "    hex ( %s ) (%s %s %s) simpleGrading (%s %s %s)" % \
                         (conn, self.nx, self.ny, self.nz, self.grad_x, self.grad_y, self.grad_z)
points = []
cells = []
patches = []

if __name__ == '__main__':
    pnts = [Point(-304.8, 0, -300),
            Point(0, 0, -300),
            Point(12, 0, -300),
            Point(14, 0, -300),
            Point(20, 0, -300),
            Point(26, 0, -300),
            Point(32, 0, -300),
            Point(332, 0, -300)]
    points.extend(pnts)
    for z_coord in [0,2,5.5,7.5,11.,13.,23]:
        trans =  300 + z_coord 
        for pnt in pnts[:]:
            points.append(pnt.translate(z=trans))
    for pnt in points[:]:
        points.append(pnt.translate(y=10.0))
    nx = {0:100,
          1:72,
          2:12,
          3:48,
          4:48,
          5:48,
          6:100}
    nz = {0:100,
          1:12,
          2:18,
          3:12,
          4:18,
          5:12,
          6:40}
    gx = {0:0.1,
          1:1,
          2:1,
          3:1,
          4:1,
          5:1,
          6:10}
    gz = {0:0.1,
          1:1,
          2:1,
          3:1,
          4:1,
          5:1,
          6:10}
    for z_layer in range(7):
        for x_layer in range(7):
            conn = [z_layer*8 + x_layer,
                    z_layer*8 + 1 + x_layer,
                    z_layer*8 + 1 + 64 + x_layer,
                    z_layer*8 + 64 + x_layer,
                    (z_layer + 1)*8 + x_layer,
                    (z_layer + 1)*8 + 1 + x_layer,
                    (z_layer + 1)*8 + 1 + 64 + x_layer,
                    (z_layer + 1)*8 + 64 + x_layer]
            cell = Cell(conn, 
                        nx[x_layer], 
                        1, 
                        nz[z_layer], 
                        grad_x = gx[x_layer], 
                        grad_z = gz[z_layer])
            cells.append(cell)
    # Delete the adiabatic blocks
    del cells[29]
    del cells[28]
    del cells[22]
    del cells[21]
    del cells[15]
    del cells[14]
    patches.append(Patch(type="symmetryPlane",
                         name = "left",
                         faces = [cells[0].f5,
                                  cells[7].f5,
                                  cells[29].f5,
                                  cells[36].f5]))
    patches.append(Patch(type="patch",
                         name = "right",
                         faces = [cells[6].f3,
                                  cells[13].f3,
                                  cells[18].f3,
                                  cells[23].f3,
                                  cells[28].f3,
                                  cells[35].f3,
                                  cells[42].f3]))
    patches.append(Patch(type="patch",
                         name = "inlet",
                         faces = [cells[0].f0,
                                  cells[1].f0,
                                  cells[2].f0,
                                  cells[3].f0,
                                  cells[4].f0,
                                  cells[5].f0,
                                  cells[6].f0]))
    patches.append(Patch(type="wall",
                         name = "ceiling",
                         faces = [cells[36].f1,
                                  cells[37].f1,
                                  cells[38].f1,
                                  cells[39].f1,
                                  cells[40].f1,
                                  cells[41].f1,
                                  cells[42].f1]))
    patches.append(Patch(type="wall",
                         name = "bottom",
                         faces = [cells[7].f1,]))
    patches.append(Patch(type="wall",
                         name = "top",
                         faces = [cells[29].f0,]))
    patches.append(Patch(type="patch",
                         name = "applied",
                         faces = [cells[14].f5,
                                  cells[19].f5,
                                  cells[24].f5]))
    patches.append(Patch(type="patch",
                         name = "adiabatic",
                         faces = [cells[8].f1,
                                  cells[30].f0]))
    front = []
    back = []
    for cell in cells:
        front.append(cell.f2)
        back.append(cell.f4)
    patches.append(Patch(type="empty",
                         name = "front",
                         faces = front))
    patches.append(Patch(type="empty",
                         name = "back",
                         faces = back))

    f = open(os.path.join(".","constant","polyMesh","blockMeshDict"), "w")
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\" + "\n")
    f.write(r"| =========                 |                                                 |" + "\n")
    f.write(r"| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |" + "\n")
    f.write(r"|  \\    /   O peration     | Version:  1.7.1                                 |" + "\n")
    f.write(r"|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |" + "\n")
    f.write(r"|    \\/     M anipulation  |                                                 |" + "\n")
    f.write(r"\*---------------------------------------------------------------------------*/" + "\n")
    f.write(r"FoamFile" + "\n")
    f.write(r"{" + "\n")
    f.write(r"    version     2.0;" + "\n")
    f.write(r"    format      ascii;" + "\n")
    f.write(r"    class       dictionary;" + "\n")
    f.write(r"    object      blockMeshDict;" + "\n")
    f.write(r"}" + "\n")
    f.write(r"// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //" + "\n")
    f.write("\n")
    f.write("convertToMeters 1;" + "\n")

    f.write("vertices\n(\n")
    for pnt in points:
        f.write(str(pnt) + "\n")
    f.write(");\n")
    f.write("blocks\n(\n")
    for index, cell in enumerate(cells):
        f.write(str(cell) + "// block %s\n" % (index))
    f.write(");\n")
    f.write("edges\n(\n);\n")
    f.write("patches\n(\n")
    for patch in patches:
        f.write(str(patch) + "\n")
    f.write(");\n")
    f.write("mergePatchPairs\n")
    f.write("(\n")
    f.write(");\n")
    f.write("\n")
    f.write("// ************************************************************************* //\n")
    f.close()

    f = open("makeCellSets.setSet", "w")
    op = "new"
    for index in [8, 9, 10, 11, 12, 14, 19, 20, 21, 24, 30, 31, 32]:
         cell = cells[index]
         f.write("cellSet heatSink %s boxToCell (%s %s %s)(%s %s %s)\n" % (op,
                                                                           points[cell.connectivity[0]].x/1000,
                                                                           points[cell.connectivity[0]].y/1000,
                                                                           points[cell.connectivity[0]].z/1000,
                                                                           points[cell.connectivity[6]].x/1000,
                                                                           points[cell.connectivity[6]].y/1000,
                                                                           points[cell.connectivity[6]].z/1000))
         op = "add"
    f.write("cellSet Air clear\n")
    f.write("cellSet Air add cellToCell heatSink\n")
    f.write("cellSet Air invert\n")
    f.close()

