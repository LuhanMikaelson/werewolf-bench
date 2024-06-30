import sys
import pandas as pd
import json
import os

def get_number_of_votes(player, votes):
    return(len([v for v in votes if v['vote'] == f'{player}.']))

def get_voter_target(player, votes):
    return([v['vote'][:-1] for v in votes if v['voter'].split()[0] == player][0])

def times_spoken(player, utterances):
    return(len([u for u in utterances if u['speaker'] == player]))

def average_utterance_length(player, utterances):
    if times_spoken(player, utterances) == 0:
        return(0)
    else:
        return(sum([len(u['utterance']) for u in utterances if u['speaker'] == player])/times_spoken(player, utterances))

def get_utterance_target(u, players):
    idxs = {}
    for p in players:
        try:
            idxs[p] = u['utterance'].index(p)
        except ValueError:
            idxs[p] = 999999
    if min(idxs.values()) == 999999:
        return('')
    return(min(idxs, key=idxs.get))

def get_utterances_asked_to_player_idx(player, utterances):
    players = list(set([u['speaker'] for u in utterances]))
    # check if player is mentioned before any other player names in each utterance, return idx if so
    return([idx for idx, u in enumerate(utterances) if get_utterance_target(u, players) == player])

def proportion_targeted_after_idx(player, utterances, idx):
    target_idx = get_utterances_asked_to_player_idx(player, utterances)
    return(len([t for t in target_idx if t > idx])/(len(utterances) - idx + 1))

def accusation_influence(player, utterances):
    acc_props = []
    players = list(set([u['speaker'] for u in utterances]))
    # for each utterance a player makes, get proportion_targeted_after_idx and average them
    for idx, u in enumerate(utterances):
        if u['speaker'] == player:
            target = get_utterance_target(u, players)
            acc_prop = proportion_targeted_after_idx(target, utterances, idx)
            acc_props.append(acc_prop)
    if len(acc_props) == 0:
        return(0)
    return(sum(acc_props)/len(acc_props))

def accusation_influence_on_votes(player, utterances, votes):
    acc_props = []
    players = list(set([u['speaker'] for u in utterances]))
    # for each utterance a player makes, get proportion_targeted_after_idx and average them
    for idx, u in enumerate(utterances):
        if u['speaker'] == player:
            target = get_utterance_target(u, players)
            acc_prop = get_number_of_votes(target, votes)
            acc_props.append(acc_prop)
    if len(acc_props) == 0:
        return(0)
    return(sum(acc_props)/len(acc_props))

def num_accusations(player, utterances):
    players = list(set([u['speaker'] for u in utterances]))
    return(len([u for u in utterances if u['speaker'] == player and get_utterance_target(u, players) != '']))

def main():
    path = sys.argv[1]
    game_id = path.split('/')[-1].replace('.json', '')
    data_save_path = sys.argv[2]
    game_type = sys.argv[3]
    game_data = json.load(open(path, 'r'))
    write_data = {
        'game_id':[],
        'game_type':[],
        'player_id':[],
        'player_name':[],
        'player_role':[],
        'number_of_votes':[],
        'target_votes':[],
        'times_spoken':[],
        'average_utterance_length':[],
        'accusation_influence':[],
        'accusation_influence_on_votes':[],
        'num_accusations':[],
        'times_accused':[]
    }
    players = list(set([u['speaker'] for u in game_data['utterances']]))

    for idx, player in enumerate(game_data['players_and_roles']):
        write_data['game_id'].append(game_id)
        write_data['game_type'].append(game_type)
        write_data['player_id'].append(idx)
        write_data['player_name'].append(player)
        write_data['player_role'].append(game_data['players_and_roles'][player])
        write_data['number_of_votes'].append(get_number_of_votes(player, game_data['votes']))
        write_data['target_votes'].append(get_number_of_votes(get_voter_target(player, game_data['votes']), game_data['votes']))
        write_data['times_spoken'].append(times_spoken(player, game_data['utterances']))
        write_data['average_utterance_length'].append(average_utterance_length(player, game_data['utterances']))
        write_data['accusation_influence'].append(accusation_influence(player, game_data['utterances']))
        write_data['accusation_influence_on_votes'].append(accusation_influence_on_votes(player, game_data['utterances'], game_data['votes']))
        write_data['num_accusations'].append(num_accusations(player, game_data['utterances']))
        write_data['times_accused'].append(len([u for u in game_data['utterances'] if get_utterance_target(u, players) == player]))
    
    if not os.path.exists(data_save_path):
        pd.DataFrame(write_data).to_csv(data_save_path, index=False)
    else:
        df = pd.read_csv(data_save_path)
        df = pd.concat([df, pd.DataFrame(write_data)], axis=0)
        df.to_csv(data_save_path, index=False)

if __name__ == '__main__':
    main()