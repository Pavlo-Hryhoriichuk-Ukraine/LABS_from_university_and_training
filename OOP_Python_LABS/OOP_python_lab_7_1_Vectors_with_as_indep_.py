import re
import numpy as np
from scipy.linalg import null_space

class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __call__(self, string: str):
        def get_val(char):
            match = re.search(fr"([+-]?\d*\.?\d*){char}", string)
            val = match.group(1) if match else "0"
            return float(val) if val not in ["", "+", "-"] else float(val + "1")
        
        self.x, self.y, self.z = get_val("i"), get_val("j"), get_val("k")

    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def __mul__(self, other):
        return Vector3D(self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)

    def __bool__(self):
        return abs(self) > 1e-10
    
    def __repr__(self):
        return f"{self.x}i + {self.y}j + {self.z}k"
    
    def to_numpy(self):
        return np.array([self.x, self.y, self.z], dtype=float)


class VectorSpace:
    def __init__(self):
        self.vectors = []
        self.matrix = None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def __call__(self, *args):
        for v in args:
            self.add_vector(v)
            
    def add_vector(self, v):
        v_col = v.to_numpy().reshape(3, 1)
        if self.matrix is None:
            self.matrix = v_col
            self.vectors.append(v)
            return

        trial_matrix = np.hstack((self.matrix, v_col))
        if np.linalg.matrix_rank(trial_matrix, tol=1e-10) > np.linalg.matrix_rank(self.matrix, tol=1e-10):
            self.matrix = trial_matrix
            self.vectors.append(v)
        else:
            temp_matrix = np.hstack((self.matrix, v_col))
            ns = null_space(temp_matrix)
            coeffs = ns[:, 0]
            indices = np.where(np.abs(coeffs) > 1e-10)[0]
            
            norms = [self.vectors[i].__abs__() if i < len(self.vectors) else v.__abs__() for i in indices]
            max_idx_in_indices = np.argmax(norms)
            idx_to_remove = indices[max_idx_in_indices]
            
            if idx_to_remove < len(self.vectors):
                self.matrix = np.delete(self.matrix, idx_to_remove, axis=1)
                self.vectors.pop(idx_to_remove)
                self.add_vector(v)
            else:
                pass

if __name__ == "__main__":
    v1, v2, v3, v4 = Vector3D(), Vector3D(), Vector3D(), Vector3D()
    v1("3i-6j+3k"); v2("4i-5k+1j"); v3("1i-2j+7k"); v4("8i+3j+9k")
    with VectorSpace() as space:
        space(v1, v2, v3, v4)
        print("Результат:", space.vectors)