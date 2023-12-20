import subprocess
import ray

def start_ray_head(cpus):
    subprocess.run(["ray", "stop"])
    subprocess.run(["ray", "start", "--head", f"--num-cpus={cpus}"])

def run_your_code():
    subprocess.run(["python3", "julia_ray.py"])

def main():
    cpus = 4
    for _ in range(6): 
        start_ray_head(cpus)
        run_your_code()  
        cpus *= 2 

    subprocess.run(["ray", "stop"])

if __name__ == "__main__":
    main()
