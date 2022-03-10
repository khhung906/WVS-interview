class DataProcessor():
    def __init__(self, time_table, people, part_times, whole_times):
        self.time_table = time_table
        self.table = self.create_table()
        self.time_count = sum([sum([len(t) for t in time.values()]) for time in time_table.values()])
        self.data = [{"name": str(p[0]), "time": []} for p in people.values.tolist()]
        self.part_times = part_times
        self.whole_times = whole_times
        
    def create_table(self):
        def acc(time_list, cnt):
            return list(range(cnt, cnt+len(time_list))), cnt+len(time_list)

        count = 0
        day_311, count = acc(self.time_table["3/11"]["day"], count)
        morning_312, count = acc(self.time_table["3/12"]["morning"], count)
        afternoon_312, count = acc(self.time_table["3/12"]["afternoon"], count)
        morning_313, count = acc(self.time_table["3/13"]["morning"], count)
        afternoon_313, count = acc(self.time_table["3/13"]["afternoon"], count)

        count = 0
        time_label = {}
        time_list = []
        for time in self.time_table:
            for tt in self.time_table[time]:
                for t in self.time_table[time][tt]:
                    time_list.append(f'{time}_{t}')
                    time_label[f'{time}_{t}'] = count
                    count += 1

        table = {
            "3/11_day": day_311,
            "3/12_morning": morning_312,
            "3/12_afternoon": afternoon_312,
            "3/13_morning": morning_313,
            "3/13_afternoon": afternoon_313,
            "time_label": time_label,
            "time_list": time_list
        }

        return table

    def whole_time_index(self, reply, time):
        if reply == "全天都可以" or reply == "所有時段都可以":
            if time == "3/11（五）19:00-21:30": 
                return self.table["3/11_day"]
            elif time == "3/12（六）9:35-12:25 & 13:30-16:55": 
                return self.table["3/12_morning"] + self.table["3/12_afternoon"]
            elif time == "3/13（日）9:00-12:25 & 13:30-16:55": 
                return self.table["3/13_morning"] + self.table["3/13_afternoon"]

        elif reply == "上午時段都可以（下一頁填寫下午可面試時間）":
            if time == "3/12（六）9:35-12:25 & 13:30-16:55": 
                return self.table["3/12_morning"]
            elif time == "3/13（日）9:00-12:25 & 13:30-16:55": 
                return self.table["3/13_morning"]
        
        elif reply == "下午時段都可以（下一頁填寫上午可面試時間）" or reply == "下午時段都可以（下一頁上午可面試時間）":
            if time == "3/12（六）9:35-12:25 & 13:30-16:55": 
                return self.table["3/12_afternoon"]
            elif time == "3/13（日）9:00-12:25 & 13:30-16:55": 
                return self.table["3/13_afternoon"]

        elif reply == "都不行QQ" or reply == "部分時段可以（下一頁填寫詳細時間）" or reply == "只有幾個時段可以（下一頁填寫詳細時間）":
            return []

        raise Exception('Unknown reply:', reply)

    def part_time_index(self, reply, time):
        def isNaN(num):
            return num != num
        def change_dash(word):
            w = list(word)
            if w[5] == '~':
                w[5] = '-'
            elif w[4] == '~':
                w[4] = '-'
            return "".join(w)

        if isNaN(reply) or reply == "都不行...":
            return []

        indices = []
        for t in reply.split(", "):
            indices.append(self.table["time_label"][f"{time[:4]}_{change_dash(t)}"])

        return indices

    def transform_data(self):
        # whole day
        for time in self.whole_times:
            for idx, reply in enumerate(self.whole_times[time].tolist()):
                indices = self.whole_time_index(reply, time)
                for index in indices:
                    self.data[idx]["time"].append(index)

        # half day
        for time in self.part_times:
            for idx, reply in enumerate(self.part_times[time].tolist()):
                indices = self.part_time_index(reply, time)
                for index in indices:
                    self.data[idx]["time"].append(index)

        # sort all the time of all people
        for dat in self.data:
            dat["time"].sort()


    def res_output(self, result, path):
        fp = open(path, 'w+')
        # print(result)
        for res in result.keys():
            line = self.table["time_list"][res] + ' ' * 3
            for p in result[res]:
                line += ' '+p
            line += '\n'
            fp.write(line)
