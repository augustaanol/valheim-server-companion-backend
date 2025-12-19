import re


def parse_players(text: str):
    players = []

    # Podziel po liniach, pomijając pierwszą (Online X)
    lines = text.strip().split("\n")[1:]

    for line in lines:
        player = {}

        # Name = pierwsze słowo w linii
        match_name = re.match(r"(\S+)\s", line)
        if match_name:
            player["name"] = match_name.group(1)

        # Steam ID
        match_steam = re.search(r"Steam ID:(\d+)", line)
        if match_steam:
            player["steam_id"] = match_steam.group(1)

        # Position (x y z)
        match_pos = re.search(
            r"Position:\s*\(([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\)", line
        )
        if match_pos:
            player["position"] = (
                float(match_pos.group(1)),
                float(match_pos.group(2)),
                float(match_pos.group(3)),
            )

        # Rotation (0,16)
        match_rot = re.search(r"Position:.*\)\((\d+),(\d+)\)", line)
        if match_rot:
            player["rotation"] = (
                float(match_rot.group(1)),
                float(match_rot.group(2)),
            )

        # Player ID
        match_pid = re.search(r"Player ID:(\d+)", line)
        if match_pid:
            player["player_id"] = int(match_pid.group(1))

        # HP
        match_hp = re.search(r"HP:([-\d\.]+)/([-\d\.]+)", line)
        if match_hp:
            player["hp"] = (
                int(float(match_hp.group(1))),
                int(float(match_hp.group(2))),
            )

        players.append(player)

    return players
