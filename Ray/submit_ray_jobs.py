import subprocess
import ray

def start_ray_head(cpus):
    # Stop any existing Ray processes
    subprocess.run(["ray", "stop"])
    
    # Start Ray head with specified number of CPUs
    subprocess.run(["ray", "start", "--head", "--num-cpus={}".format(cpus)])

def run_your_code():
    # Execute the julia_ray.py script
    subprocess.run(["python3", "julia_ray.py"])

def main():
    cpus = 4
    for _ in range(6):  # Adjust the range as needed
        start_ray_head(cpus)
        run_your_code()  # Call the function to execute your Python script
        cpus *= 2  # Double the number of CPUs

    # Stop Ray when done
    subprocess.run(["ray", "stop"])

if __name__ == "__main__":
    main()
