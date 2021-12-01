from interface import *
import heapq

def breadth_first(grid,explored_next,visited,end,generation,back_track):
    if not end :
        queue = []
        for current in explored_next:
            current.update_neighbor(grid)
            if not current.generation:
                current.father(generation)
            for node in current.neighbors:
                if node not in visited:
                    queue.append(node)
                if node.color == TURQUOISE:
                    end = current
                    end.color = RED
                node.open_path()
            visited.add(current)
        explored_next = set()
        generation += 1

        for node in queue:
            explored_next.add(node)
            node.open_path()

        for node in visited:
            node.explored()
    else:
        back_track.add(end)
        if end.generation > 0:
            for back_node in end.neighbors:
                back_node.update_neighbor(grid)
                back_node.explored()
                if back_node.generation:
                    if back_node.generation < end.generation:
                        end = back_node
        for node in back_track:
            node.color = RED
    return explored_next,visited,end,generation,back_track

def deep_first(grid,explored_next,visited,end,generation,current_node,back_track):
    if not end :
        current_node.update_neighbor(grid)
        for node in current_node.neighbors:
            if not node.generation:
                node.generation = generation
            if node.color == TURQUOISE:
                end = node
                end.update_neighbor(grid)
            if node not in visited and node not in explored_next:
                explored_next.insert(0,node)
            node.open_path()
        
        visited.append(current_node)
        explored_next.remove(current_node)
        
        if explored_next:
            current_node = explored_next[0]

        for node in visited:
            node.explored()
        generation += 1
        
    else:
        back_track.add(end)
        if end.generation > 0:
            for back_node in end.neighbors:
                back_node.update_neighbor(grid)
                back_node.explored()

                if back_node.generation:
                    if back_node.generation < end.generation:
                        end = back_node
        for node in back_track:
            node.color = RED
    return explored_next,visited,end,generation,current_node,back_track

def dijktra(grid,current_node,explored_next,visited,end,back_track):
    if not end:
        current_node[1].update_neighbor(grid)
        for node in current_node[1].neighbors:
            if not node.distance_from_start:
                node.distance_from_start = current_node[1].distance_from_start + node.weight
            if node.color == TURQUOISE:
                end = node
                end.update_neighbor(grid)
            if not any(node in node_tuple for node_tuple in visited) and not any(node in node_tuple for node_tuple in explored_next):
                heapq.heappush(explored_next,(node.distance_from_start,node))
            node.open_path()

        visited.add(current_node)
        current_node = heapq.heappop(explored_next)

        for node in visited:
            node[1].explored()
    
    else:
        back_track.add(end)
        if end.distance_from_start > 0:
            for neighbor in end.neighbors:
                neighbor.update_neighbor(grid)
                if neighbor.distance_from_start:
                    if neighbor.distance_from_start <= end.distance_from_start:
                        end = neighbor
                        diff_to_end=end.distance_from_start - neighbor.distance_from_start 
                        end.distance_from_start = end.distance_from_start - diff_to_end
            for node in back_track:
                node.color = RED

    return explored_next,visited,current_node,end,back_track

def a_star(grid,current_node,explored_next,visited,end,back_track,pos_end_node):
    if not end:
        current_node[1].update_neighbor(grid)
        for node in current_node[1].neighbors:
            node.distance_from_end = abs(node.row - pos_end_node[0]) + abs(node.column - pos_end_node[1])
            if not node.distance_from_start:
                node.distance_from_start = current_node[1].distance_from_start + node.weight
            if not node.heuristic_distance:
                node.heuristic_distance = node.distance_from_start + node.distance_from_end
            if node.color == TURQUOISE:
                end = node
                end.update_neighbor(grid)
            if not any(node in node_tuple for node_tuple in visited) and not any(node in node_tuple for node_tuple in explored_next):
                heapq.heappush(explored_next,(node.heuristic_distance,node))
            node.open_path()

        visited.add(current_node)
        current_node = heapq.heappop(explored_next)

        for node in visited:
            node[1].explored()
    
    else:
        back_track.add(end)
        if end.distance_from_start > 0:
            for neighbor in end.neighbors:
                neighbor.update_neighbor(grid)
                if neighbor.distance_from_start:
                    if neighbor.distance_from_start <= end.distance_from_start:
                        end = neighbor
                        diff_to_end=end.distance_from_start - neighbor.distance_from_start 
                        end.distance_from_start = end.distance_from_start - diff_to_end
            for node in back_track:
                node.color = RED

    return explored_next,visited,current_node,end,back_track