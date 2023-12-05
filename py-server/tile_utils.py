def cheb_dist(pos1, pos2):
    """
    Calculate the Chebyshev distance between two positions.

    :param pos1: First position as a tuple (x1, y1).
    :param pos2: Second position as a tuple (x2, y2).
    :return: Chebyshev distance between pos1 and pos2.
    """
    print(pos1)
    print(pos2)
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))