class Solver(object):
    def __init__(self, data, cnt_time, lower_bound, upper_bound):
        self.cnt_time = cnt_time
        # sort with time table -> most time -> least time (early time -> late time)
        self.data = sorted(data, key=self.sort_time)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        print(self.data)

    def sort_time(self, elem):
            spare_time = len(elem["time"])
            first_time = elem["time"][0]
            return spare_time*100+first_time

    def solve(self):
        def _sort(time): 
            if cnts[time] < self.lower_bound:
                return 100*(self.lower_bound-cnts[time])
            return 0

        def _solve(p_idx):
            if p_idx >= len(self.data):
                return True
            for o in sorted(self.data[p_idx]['time'], key=_sort):
                if cnts[o] >= self.upper_bound:
                    continue
                cnts[o] += 1
                alloc[o].append(self.data[p_idx]['name'])
                if _solve(p_idx+1):
                    return True
                cnts[o] -= 1
                alloc[o].remove(self.data[p_idx]['name'])
            return False

        cnts = [0]*self.cnt_time
        alloc = {i:[] for i in range(self.cnt_time)}

        if _solve(0):
            return alloc
        else:
            print('Match Fails')
