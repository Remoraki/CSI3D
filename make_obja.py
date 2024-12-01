from .decompression import main_pipeline as mp
from .objc.objc import Objc
from tqdm import tqdm

import argparse

def main (args) : 
    input_file = args.file_name
    output_file = args.output_file
    objc = Objc()
    
    total = 0
    with open(input_file, 'r') as fp:
        total = len(fp.readlines())

    
    
    parser = objc.open_objc_from_path(input_file)
    next(parser)
    
    # write the initialization : 
    graph = objc.graph
    
    create_file = open(output_file, "w")
    create_file.close()     
    
    for v in objc.verticies :
        if v is not None :
            with open(output_file, "a") as f :
                f.write(f"v {float(v.x)} {float(v.y)} {float(v.z)}\n")
    
    for f in objc.faces :
        if f is not None : 
            with open(output_file, "a") as f_ :
                f_.write(f"f {f[0]+1} {f[1]+1} {f[2]+1}\n") 
    
    
    with open(output_file, "a") as f :
        with tqdm(total=total) as pbar:
            while True : 
                pbar.update(1)
                try : 
                    coord_bary_sorted, removed_faces, final_added_faces = mp.pipeline(objc, parser)
                
                    for bary in coord_bary_sorted :
                        f.write(f"v {float(bary.x)} {float(bary.y)} {float(bary.z)}\n")
                        
                    for sublist in removed_faces :
                        for idx in sublist :
                            f.write(f"df {idx+1}\n")
                            
                    for face in final_added_faces :
                        f.write(f"f {face.x+1} {face.y+1} {face.z+1}\n")
                
                except StopIteration :
                    break
                

if __name__ == "__main__" : 
    parser = argparse.ArgumentParser(description='Decompress a .objc file')
    parser.add_argument('file_name', type=str, help='The path to the file to decompress')
    parser.add_argument('output_file', type=str, help='The path to the output file')
    args = parser.parse_args()
    main(args)    