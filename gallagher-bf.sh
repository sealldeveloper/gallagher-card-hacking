#!/bin/bash
pid=0
countto=100
# Function to handle the interrupt signal
interrupt_handler() {
    echo -e "\nScript interrupted. Exiting..."
    kill $pid
    exit 0
}

# Set up the interrupt handler
trap interrupt_handler SIGINT

# Check if the script is run with sudo privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo privileges."
    exit 1
fi

# Initialize the counter
counter=300000

# Counter
while [ $counter -le $countto ]
do
    # Print the current value
    echo -ne "Card $counter\r"
    sudo python3 gallagher-encode.py --CN $counter --FC 0 --RC 1 --UB 0 --UE 0 --UC 0 --UD 0 --IL 1 --emulate-proxmark  > output.tmp 2>&1 & 
    pid=$!

    # Initialize a flag to track if we've found the phrase
    found=0

    # Continuously check the output file until we find the phrase or the script ends
    while ps -p $pid > /dev/null 2>&1; do
        if grep -q "Press" output.tmp; then
            echo -e "Card $counter - Ready!\r"
            found=1
            break
        fi
        sleep 0.1
    done

    # Wait for the Python script to finish
    wait $pid

    # Clean up the temporary output file
    rm output.tmp

    # Increment the counter
    ((counter++))
done
