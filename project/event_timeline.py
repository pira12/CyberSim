import random


def attack_generator():
    if(random.random() > 0.5):
        return 1
    else:
        return 0


def run_sim(run_time):
    current_time = 0
    while(current_time < run_time):
        if(attack_generator()):
            event_list.append(f"Attack is generated at time {current_time}")

        current_time += 1

def print_event_list(event_list):
    for event in event_list:
        print(event)


if __name__ == "__main__":
    total_run_time = 30
    event_list = []
    run_sim(total_run_time)
    print_event_list(event_list)