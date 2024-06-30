import sys
import json

def get_players_and_roles(transcript_list):
    players = {}
    day_start_idx = transcript_list.index('>***GAME:*** Everyone, Wake up!\n')
    for line in transcript_list[:day_start_idx]:
        if line.startswith('Player number') and line.endswith('card.\n'):
            player = line.split(' ')[5].replace(',', '')
            role = line.split(' ')[-2]
            players[player] = role    
    return players

def get_list_of_utterances(transcript_list):
    utterances = []
    day_start_idx = transcript_list.index('>***GAME:*** Everyone, Wake up!\n')
    day_end_idx = transcript_list.index('## The ***VOTE*** phase will now commence.\n')
    transcript_list = transcript_list[day_start_idx+1:day_end_idx-1]
    for idx in range(0, len(transcript_list), 2):
        thought = transcript_list[idx].split('***' )[-1]
        utterance = transcript_list[idx+1].split('** ')[-1]
        speaker = transcript_list[idx+1].split('**')[1][:-1]
        utterances.append({'speaker': speaker, 'thought': thought, 'utterance': utterance, 'idx': idx//2})
    return utterances

def get_list_of_votes(transcript_list):
    vote_start_idx = transcript_list.index(">***GAME:*** It's time to vote!\n")
    vote_end_idx = transcript_list.index('The votes were:\n')
    transcript_list = transcript_list[vote_start_idx+1:vote_end_idx]
    votes = []
    for idx in range(0, len(transcript_list), 2):
        thought = transcript_list[idx].split('***' )[-1]
        vote = transcript_list[idx+1].split()[-1]
        voter = transcript_list[idx+1].split('**')[1][:-1]
        votes.append({'voter': voter, 'thought': thought, 'vote': vote, 'idx': idx//2})
    return votes

def get_player_role_information(transcript_list):
    role_information = []
    night_start_idx = transcript_list.index('>***GAME:*** Everyone, close your eyes.\n')
    night_end_idx = transcript_list.index('## The ***DAY*** phase will now commence.\n')
    transcript_list = transcript_list[night_start_idx:night_end_idx]
    player_role_info = {}
    for line in transcript_list:
        if 'aware' in line or 'looked at' in line or 'randomly viewed' in line:
            role_information.append(line)
    return role_information

def main():
    path = sys.argv[1]
    save_path = f"game_jsons/{'/'.join(path.split('/')[-2:])}".replace('.md', '.json')
    with open(path, 'r') as f:
        transcript = f.readlines()
    transcript = [line for line in transcript if line != '\n']

    players_and_roles = get_players_and_roles(transcript)
    role_information = get_player_role_information(transcript)
    list_of_utterances = get_list_of_utterances(transcript)
    list_of_votes = get_list_of_votes(transcript)
    
    data = {'players_and_roles': players_and_roles, 'player_role_information':role_information, 'utterances': list_of_utterances, 'votes': list_of_votes}
    with open(save_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    main()