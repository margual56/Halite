"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
    2.a. Try to Dock in the planet if close enough
    2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
import hlt
import logging

import time


def getDocked(game):
    dockedShips = []
    freeShips = []

    allShips = game.get_me().all_ships()

    for ship in allShips:
        if ship.docking_status == ship.DockingStatus.UNDOCKED or ship.docking_status == ship.DockingStatus.UNDOCKING:
            dockedShips.append(ship)
        else:
            freeShips.append(ship)

    return dockedShips, freeShips


def getPlanets(game):
    available = []
    mine = []
    others = []

    allPlanets = game.all_planets()

    for planet in allPlanets:
        if not planet.is_owned():
            available.append(planet)
        elif planet.owner == game.get_player():
            mine.append(planet)
        else:
            others.append(planet)

    return available, mine, others


def getEnemyShips(game):
    players = game.all_players()
    players.remove(game.get_me())

    allShips = []

    for player in players:
        allShips.append(player.all_ships())

    return allShips


def getClosestPlanet(game, ship):
    # El problema es que primero tienen que navegar hacia ese planeta, pero si cada turno les asignamos a cada nave un planeta
    # aleatorio, va a andar cambiando constantemente. Tal vez hacer una lista ordenada(?) O tal vez ponerle a las Ships una variable
    # Además, debería de coger algún planeta que no esté libre, por tener varias naves por planeta... pensé en hacerlo con un
    # if random()<0.5 then freePlanets else myPlanets, sabes?
    planets = game.all_planets()
    freePlanets
    for planet in planets:



def calculateNumberDocked(game, conquered, available, docked, availableShips, totalShips, turnNumber):
    '''
    :param game:
    :param myPlanets:
    :param availablePlanets:
    :param dockedShips:
    :param freeShips:
    :param turnNumber:
    :return:
    '''

    '''
    If n2 <= 0 Or n4 <= 0 Then
        Halite = n3
    ElseIf n3 <= 6 Then
        Halite = n5 * 0.55
    Else
        Halite = WorksheetFunction.Min((n2 * n1 / n3) / 2 + n3, n4)
    End If
    '''

    if  available == 0 or totalShips == 0:
        return docked
    elif availableShips <=6:
        return totalShips*0.55
    else:
        return min((available * conquered / docked) / 2 + docked, availableShips)


def main():
    # GAME START
    # Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
    game = hlt.Game("Aggressive")
    # Then we print our start message to the logs
    logging.info("Starting my aggressive bot!")

    turn = 0

    while True:
        turn += 1

        # TURN START
        # Update the map for the new turn and get the latest version
        game_map = game.update_map()

        intialTime = time.clock_gettime()

        shipsDocked, shipsFree = getDocked(game_map)
        enemyShips = getEnemyShips(game_map)
        planetsAvailable, planetsConquered, planetsEnemy = getPlanets(game_map)

        dockedGoal = calculateNumberDocked(game_map, len(planetsConquered), len(planetsAvailable), len(shipsDocked), len(shipsFree), turn)

        # Here we define the set of commands to be sent to the Halite engine at the end of the turn
        command_queue = []

        dockedDifference = dockedGoal - len(shipsDocked)

        # if we need more ships on planets
        if dockedDifference>0:
            count = dockedDifference
            for ship in shipsFree:
                command_queue.append(ship.dock(getClosestPlanet(game_map, ship)))

        # For every ship that I control
        for ship in :
            # If the turn is taking more than 1.5 seconds
            if time.clock_gettime()-intialTime > 1.5:
                break

            # If the ship is docked
            if ship.docking_status != ship.DockingStatus.UNDOCKED:
                # Skip this ship
                continue

            # For each planet in the game (only non-destroyed planets are included)
            for planet in game_map.all_planets():
                # If the planet is owned
                if planet.is_owned():
                    # Skip this planet
                    continue

                # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
                if ship.can_dock(planet):
                    # We add the command by appending it to the command_queue
                    command_queue.append(ship.dock(planet))
                else:
                    # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                    # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                    # We run this navigate command each turn until we arrive to get the latest move.
                    # Here we move at half our maximum speed to better control the ships
                    # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                    # This will mean that you have a higher probability of crashing into ships, but it also means you will
                    # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                    # wish to turn that option off.
                    navigate_command = ship.navigate(
                        ship.closest_point_to(planet),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=True)
                    # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                    # or we are trapped (or we reached our destination!), navigate_command will return null;
                    # don't fret though, we can run the command again the next turn)
                    if navigate_command:
                        command_queue.append(navigate_command)
                break

        # Send our set of commands to the Halite engine for this turn
        game.send_command_queue(command_queue)
        # TURN END
    # GAME END


if __name__ == '__main__':
    main()