import os
import filecmp
import shutil # library to managmant files inside folders
import time # library to get time to log file
import argparse # library to add coments in cmd (path, period etc)
import atexit # give a message when shut down process
import traceback

## Please implement a program that synchronizes two folders: source and 
## replica. The program should maintain a full, identical copy of source 
## folder at replica folder. Solve the test task by writing a program in 
## Pythons

def synchronizer(source, replica, logger):

    log = open(logger, "a")                      
    # Take time to add this info in logger
    current_time = time.strftime("%H:%M:%S") 
    
    # Create the replica folder if it doesn't exist
    if not os.path.exists(replica):
        os.makedirs(replica)
        log.write(f"{current_time}: Created replica folder\n")
        print(f"{current_time}: Created replica folder")
                
    # Compare source and replica folders
    dist_compare = filecmp.dircmp(source, replica)  
    # Section to create new subfolders and copy files to replica
    for name in dist_compare.left_only:
        source_path = os.path.join(source, name)
        destination_path = os.path.join(replica, name)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
            log.write(f"{current_time}: Created folder: {source_path} -> {destination_path}\n")
            print(f"{current_time}: Created folder: {source_path} -> {destination_path}")
        else:
            shutil.copy2(source_path, destination_path)
            log.write(f"{current_time}: Copied file: {source_path} -> {destination_path}\n")
            print(f"{current_time}: Copied file: {source_path} -> {destination_path}")
            
    
    # Section to remove subfolders and files from replica
    for name in dist_compare.right_only:
        replica_path = os.path.join(replica, name)
        if os.path.isdir(replica_path):
            shutil.rmtree(replica_path)
            log.write(f"{current_time}: Removed folder: {replica_path}\n")
            print(f"{current_time}: Removed folder: {replica_path}")
        else:
            os.remove(replica_path)
            log.write(f"{current_time}: Removed file: {replica_path}\n")
            print(f"{current_time}: Removed file: {replica_path}")

    # Update files replica
    source_files = os.listdir(source)
    for name in source_files:
        source_path = os.path.join(source, name)
        destination_path = os.path.join(replica, name)
        if not os.path.isdir(source_path) and os.path.getmtime(source_path) > os.path.getmtime(destination_path):
            shutil.copy2(source_path, destination_path)
            log.write(f"{current_time}: Update file: {source_path} -> {destination_path}\n")
            print(f"{current_time}: Update file: {source_path} -> {destination_path}")

def synchronize_subfolders(source, replica, logger):
    log = open(logger, "a") 
    current_time = time.strftime("%H:%M:%S")

    # Create a list of subfolders in the source folder as strings
    source_subfolders = []
    for dp, dn, _ in os.walk(source):
        for dn_entry in dn:
            subfolder_path = os.path.join(dp, dn_entry)
            source_subfolders.append(subfolder_path)

    # Create a list of subfolders in the replica folder as strings
    replica_subfolders = []
    for dp, dn, _ in os.walk(replica):
        for dn_entry in dn:
            subfolder_path = os.path.join(dp, dn_entry)
            replica_subfolders.append(subfolder_path)

    # Compare source_subfolders and replica_subfolders
    for source_folder, replica_folder in zip(source_subfolders, replica_subfolders):
        dcmp = filecmp.dircmp(source_folder, replica_folder)

        # Section to create and copy file from subfolders in source to replica
        for name in dcmp.left_only:
            source_path = os.path.join(source_folder, name)
            dest_path = os.path.join(replica_folder, name)

            if os.path.isdir(source_path):
                os.makedirs(dest_path)
                log.write(f"{current_time}: Created folder: {dest_path}\n")
                print(f"{current_time}: Created folder: {dest_path}")
            else:
                shutil.copy2(source_path, dest_path)
                log.write(f"{current_time}: Copied file: {source_path} -> {dest_path}\n")
                print(f"{current_time}: Copied file: {source_path} -> {dest_path}")

        # Section to remove files and subfolders from replica
        for name in dcmp.right_only:
            path = os.path.join(replica_folder, name)
            if os.path.isdir(path):
                shutil.rmtree(path)
                log.write(f"{current_time}: Removed folder: {path}\n")
                print(f"{current_time}: Removed folder: {path}")
            else:
                os.remove(path)
                log.write(f"{current_time}: Removed file: {path}\n")
                print(f"{current_time}: Removed file: {path}")

        # Update files in subfolders
        source_files = os.listdir(source_folder)
        for name in source_files:
            source_path = os.path.join(source_folder, name)
            destination_path = os.path.join(replica_folder, name)
            if not os.path.isdir(source_path) and os.path.getmtime(source_path) > os.path.getmtime(destination_path):
                shutil.copy2(source_path, destination_path)
                log.write(f"{current_time}: Update file: {source_path} -> {destination_path}\n")
                print(f"{current_time}: Update file: {source_path} -> {destination_path}")
                 
# Section to write inputs by user
def main():
    parser = argparse.ArgumentParser(description="Synchronizer two folders")
    parser.add_argument("source", help="Path to source")
    parser.add_argument("replica", help="Path to replica")
    parser.add_argument("period", type=int, help="Synchronization period") # Must be numeric value, time in seconds
    parser.add_argument("logger", help="Log file path")
    
    args = parser.parse_args()

    start_time = time.strftime("%Y-%m-%d %H:%M:%S")
    # Create logger.txt file if no exist
    if not os.path.exists(args.logger):
        with open(args.logger, 'a') as log:
            log.write(f"{start_time}: Log file created\n")  
            print(f"{start_time}: Log file created")
            
    # Check if source_folder path exists
    log = open(args.logger, "a")  
    if not os.path.exists(args.source):
        log.write(f"{start_time}: Source folder path '{args.source}' does not exist\n")
        print(f"{start_time}: Source folder path '{args.source}' does not exist")
        return
    
    # Check if source_folder and replica_folder have different paths
    if os.path.abspath(args.source) == os.path.abspath(args.replica):
        log.write(f"{start_time}: Source folder and replica folder must have different paths\n")
        print(f"{start_time}: Source folder and replica folder must have different paths")
        return
    
    # Check if source_folder and log_file are not inside replica_folder
    if os.path.commonpath([os.path.abspath(args.source), os.path.abspath(args.logger)]) == os.path.abspath(args.replica):
        log.write(f"{start_time}: Source folder and log file must not be inside the replica folder\n")
        print(f"{start_time}: Source folder and log file must not be inside the replica folder")
        return

    # Check if period is non-negative
    if args.period < 0:
        log.write(f"{start_time}: Synchronization interval must be a non-negative integer\n")
        print(f"{start_time}: Synchronization interval must be a non-negative integer")
        return
    
    # Write a message that procees is launched
    log.write(f"{start_time}: Synchronization process launched\n")
    print(f"{start_time}: Synchronization process launched")
    
    # Give an infromation in logger when program stop
    def stop_function():
        stop_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{stop_time}: Synchronization process stopped\n")
        print(f"{stop_time}: Synchronization process stopped")
        log.close()

    atexit.register(stop_function)
    
    while True:
        current_time = time.strftime("%H:%M:%S")              
        try:       
            synchronizer(args.source, args.replica, args.logger)
            synchronize_subfolders(args.source, args.replica, args.logger)
            log.write(f"{current_time}: Synchronization complete\n")
            print(f"{current_time}: Synchronization complete")

        except Exception as e:
                log.write(f"{current_time}: Error during synchronization: {str(e)}\n")
                print(f"{current_time}: Error during synchronization: {str(e)}")
                traceback.print_exc()

        time.sleep(args.period)


if __name__ == "__main__":
    main()
