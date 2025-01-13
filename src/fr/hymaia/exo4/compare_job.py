import time
import subprocess


def execute_job(job_name, cmd):
    print(f"Exécution de {job_name}...")
    
    # timer
    start_time = time.time()

    # subprocess pour afficher les res (print) meme dans le terminal WSL
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)


    elapsed_time = time.time() - start_time
    print(f"Temps d'exécution pour {job_name}: {elapsed_time:.2f} secondes\n")
    
    if result.stdout:
        print(f"Sortie standard de {job_name}:\n{result.stdout}")
    if result.stderr:
        print(f"Sortie d'erreur de {job_name}:\n{result.stderr}")
    
    return elapsed_time

def main():
    # les job + cmd poetry
    jobs = [
        {"name": "UDF Scala", "command": "poetry run scala_udf"},
        {"name": "UDF Python", "command": "poetry run python_udf"},
        {"name": "Sans UDF", "command": "poetry run no_udf"}
    ]
    
    job_times = {}

    for job in jobs:
        job_name = job["name"]
        command = job["command"]
        elapsed_time = execute_job(job_name, command)
        job_times[job_name] = elapsed_time

    # Trie plus rapide moins rapide
    sorted_jobs = sorted(job_times.items(), key=lambda x: x[1])

    # print final pour support visuel
    print("\nRésumé des temps d'exécution (classé par temps croissant):")
    for job_name, elapsed_time in sorted_jobs:
        print(f"{job_name}: {elapsed_time:.2f} secondes")


# GG
if __name__ == "__main__":
    main()
