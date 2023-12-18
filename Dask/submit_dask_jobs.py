import subprocess
import sys
import time
import re

def reserve_oar_resources(cores, IP_address):
    reservation_command = f"oarsub -l host=2/core={cores},walltime=1 'source env/bin/activate; dask worker  {IP_address}'"
    return subprocess.run(reservation_command, shell=True, capture_output=True, text=True)

def run_julia_dask_script(IP_address):
    subprocess.run(f'python3 julia_dask.py {IP_address}', shell=True)

def delete_oar_job(job_id):
    delete_command = f"oardel {job_id}"
    subprocess.run(delete_command, shell=True)

def get_job_id(reservation_output):
    # Use regular expression to find the job ID
    match = re.search(r'OAR_JOB_ID=(\d+)', reservation_output)
    if match:
        return match.group(1)  # Return the job ID
    else:
        raise ValueError("Job ID not found in reservation output")

def wait_for_job(job_id):
    job_running = False
    while not job_running:
        # Check the status of the job
        status_command = f"oarstat -j {job_id}"
        result = subprocess.run(status_command, shell=True, capture_output=True, text=True)
        
        # Parse the output to check if the job is running
        if str(job_id) in result.stdout and ' R ' in result.stdout:
            job_running = True
        else:
            print(f"Job {job_id} not ready yet. Waiting...")
            time.sleep(10)  # Wait for 6 seconds before checking again
def main():
    cores = 2  # Starting number of cores
    for _ in range(6):  # Adjust the range as needed
        print(f"=============================================\n Reserving resources with {cores} cores")
        reservation_result = reserve_oar_resources(cores , sys.argv[1])
        try:
            job_id = get_job_id(reservation_result.stdout)
        except ValueError:
            print("Reservation failed.")
            exit()

        wait_for_job(job_id)

        print("Running script on new resources...")
        run_julia_dask_script(sys.argv[1])

        delete_oar_job(job_id)
        print(f"Deleting job with ID {job_id}")

        cores *= 2

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("IP address required")
        exit()
    main()
