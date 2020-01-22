import struct


class STLUtils:

    def signedVolumeOfTriangle(self, p1, p2, p3):
        v321 = p3[0] * p2[1] * p1[2]
        v231 = p2[0] * p3[1] * p1[2]
        v312 = p3[0] * p1[1] * p2[2]
        v132 = p1[0] * p3[1] * p2[2]
        v213 = p2[0] * p1[1] * p3[2]
        v123 = p1[0] * p2[1] * p3[2]
        return (1.0 / 6.0) * (-v321 + v231 + v312 - v132 - v213 + v123)

    def unpack(self, sig, l):
        s = self.f.read(l)
        self.fb.append(s)
        return struct.unpack(sig, s)

    def read_triangle(self):
        n = self.unpack("<3f", 12)
        p1 = self.unpack("<3f", 12)
        p2 = self.unpack("<3f", 12)
        p3 = self.unpack("<3f", 12)
        b = self.unpack("<h", 2)

        self.normals.append(n)
        l = len(self.points)
        self.points.append(p1)
        self.points.append(p2)
        self.points.append(p3)
        self.triangles.append((l, l + 1, l + 2))
        self.bytecount.append(b[0])
        return self.signedVolumeOfTriangle(p1, p2, p3)

    def read_length(self):
        length = struct.unpack("@i", self.f.read(4))
        return length[0]

    def read_header(self):
        self.f.seek(self.f.tell() + 80)

    def calculate_volume(self, infilename):
        print(infilename)
        self.normals = []
        self.points = []
        self.triangles = []
        self.bytecount = []
        self.fb = []
        totalVolume = 0
        self.f = open(infilename, "rb")
        self.read_header()
        self.read_length()
        try:
            while True:
                totalVolume += self.read_triangle()
        except Exception:
            pass
        totalVolume = (totalVolume / 1000)
        return totalVolume
