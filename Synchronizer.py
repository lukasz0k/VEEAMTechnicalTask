import os
import filecmp
import shutil # library to managmant files inside folders
import time # library to get time to log file
import argparse # library to add coments in cmd (path, period etc)
import atexit # give a message when shut down process

## Please implement a program that synchronizes two folders: source and 
## replica. The program should maintain a full, identical copy of source 
## folder at replica folder. Solve the test task by writing a program in 
## Pythons

def synchronizer(source, replica, period, logger):
    # Give the message in logger, that program is started   
    log = open(logger, "a")    
    start_time = time.strftime("%Y-%m-%d %H:%M:%S")
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
        # Take time to add this info in logger
        current_time = time.strftime("%H:%M:%S") 
        
        # Create the replica folder if it doesn't exist
        if not os.path.exists(replica):
            os.makedirs(replica)
            log.write(f"{current_time}: Created replica folder\n")
            print(f"{current_time}: Created replica folder")
        
        try:            
            changes_flag = False # Flag for changes, by default False
            # Compare source and replica folders
            dist_compare = filecmp.dircmp(source, replica)  
            # Section to create new subfolders and copy files to replica
            for name in dist_compare.left_only:
                source_path = os.path.join(source, name)
                destination_path = os.path.join(replica, name)
                changes_flag = True
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
                changes_flag = True
                if os.path.isdir(replica_path):
                    shutil.rmtree(replica_path)
                    log.write(f"{current_time}: Removed folder: {replica_path}\n")
                    print(f"{current_time}: Removed folder: {replica_path}")
                else:
                    os.remove(replica_path)
                    log.write(f"{current_time}: Removed file: {replica_path}\n")
                    print(f"{current_time}: Removed file: {replica_path}")
            
            # Give an information that all of processes are finished
            if changes_flag:
                log.write(f"{current_time}: Synchronization complete\n")
                print(f"{current_time}: Synchronization complete")
             
            # Section to write a message to user that synchronization is completed, no changes in replica folder
            if not changes_flag:
                log.write(f"{current_time}: Synchronization complete, no changes occured\n")
                print(f"{current_time}: Synchronization complete, no changes occured")
        
        # Section to write exception in synchronization process
        except Exception as e:
            log.write(f"Error during synchronization: {str(e)}\n")
            print(f"Error during synchronization: {str(e)}")
        time.sleep(period)
         
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
        with open(args.logger, 'w') as log:
            log.write(f"{start_time}: Log file created\n")  
            print(f"{start_time}: Log file created")
            
    # Check if source_folder path exists
    if not os.path.exists(args.source):
        log = open(args.logger, "a")    
        log.write(f"{start_time}: Source folder path '{args.source}' does not exist.\n")
        print(f"{start_time}: Source folder path '{args.source}' does not exist.")
        return

    # Check if period is non-negative
    if args.period < 0:
        log = open(args.logger, "a")    
        log.write(f"{start_time}: Synchronization interval must be a non-negative integer.\n")
        print(f"{start_time}: Synchronization interval must be a non-negative integer.")
        return
    
    synchronizer(args.source, args.replica, args.period, args.logger)


if __name__ == "__main__":
    main()
