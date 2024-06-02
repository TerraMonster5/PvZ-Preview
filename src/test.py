import pandas as pd
import pvz
df = pd.DataFrame(index=range(100),columns=["Zombies", "Cones", "Dolphins", "Preview Normals","Preview Cones", "Preview Dolphins"],dtype=float)
for i in range(100):
    pvz.set_internal_spawn([0,2,14])
    pvz.Sleep(2)
    zombies = list(pvz.ReadMemory("int",0x6a9ec0, 0x768, 0x6b4,array=1000))
    for k in range(20):
        ignore_rest = False
        for j in range(50):
            if (zombies[k * 50 + j] == -1):
                ignore_rest = True
                continue
            if (ignore_rest):
                zombies[k * 50 + j] = -1
    df["Zombies"][i] = zombies.count(0)
    df["Cones"][i] = zombies.count(2)
    df["Dolphins"][i] = zombies.count(14)
    preview = []
    zombies_count_max = pvz.ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x94)
    zombies_offset = pvz.ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x90)
    for j in range(zombies_count_max):
        zombie_dead = pvz.ReadMemory("bool", zombies_offset + 0xec + j * 0x15c)
        if not zombie_dead:
            zombie_type = pvz.ReadMemory("int", zombies_offset + 0x24 + j * 0x15c)
            preview.append((int)(zombie_type))
    df["Preview Normals"][i] = preview.count(0)
    df["Preview Cones"][i] = preview.count(2)
    df["Preview Dolphins"][i] = preview.count(14)
a = df.groupby(["Preview Cones","Preview Normals", "Preview Dolphins"])
print(a.size())
print(a.aggregate("mean"))


