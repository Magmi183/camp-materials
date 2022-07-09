import pandas as pd

commentary = False


def load_csv(name):
    dst = "wicked/" + name + ".csv"
    mfile = pd.read_csv(dst, sep=',')

    return mfile


if __name__ == '__main__':

    group_name = {0: "blue", 1: "green", 2: "red", 3: "yellow"}
    results = {0: 0, 1: 0, 2: 0, 3: 0}

    combos = load_csv("combos")
    default_values = load_csv("default-values")

    for group_id in range(4):

        items_build = load_csv(group_name[group_id])

        items_build['s1'] = items_build['s1'].str.upper()
        items_build['s2'] = items_build['s2'].str.upper()
        items_build['s3'] = items_build['s3'].str.upper()

        result = 0

        # s1s1 s2s2 s3s3
        # s1s1 s2s3 s3s2
        # s1s2 s2s1 s3s3
        # s1s2 s2s3 s3s1
        # s1s3 s2s1 s3s2
        # s1s3 s2s2 s3s1

        for _, build_row in items_build.iterrows():

            found_combo = False

            for _, combo_row in combos.iterrows():

                if (build_row['s1'] == combo_row['s1'] and build_row['s2'] ==
                        combo_row['s2'] and build_row['s3'] == combo_row['s3']):
                    # kek.insert(combo_row)
                    results[group_id] += combo_row['value']

                    if commentary:
                        print(f"Found combo: {combo_row['name']}")

                    found_combo = True
                    break

                if (build_row['s1'] == combo_row['s1'] and build_row['s2'] ==
                        combo_row['s3'] and build_row['s3'] == combo_row['s2']):
                    # kek.insert(combo_row)
                    results[group_id] += combo_row['value']

                    if commentary:
                        print(f"Found combo: {combo_row['name']}")

                    found_combo = True
                    break

                if (build_row['s1'] == combo_row['s2'] and build_row['s2'] ==
                        combo_row['s1'] and build_row['s3'] == combo_row['s3']):
                    # kek.insert(combo_row)

                    results[group_id] += combo_row['value']
                    if commentary:
                        print(f"Found combo: {combo_row['name']}")

                    found_combo = True
                    break

                if (build_row['s1'] == combo_row['s2'] and build_row['s2'] ==
                        combo_row['s3'] and build_row['s3'] == combo_row['s1']):
                    # kek.insert(combo_row)

                    results[group_id] += combo_row['value']

                    if commentary:
                        print(f"Found combo: {combo_row['name']}")

                    found_combo = True
                    break

                if (build_row['s1'] == combo_row['s3'] and build_row['s2'] ==
                        combo_row['s1'] and build_row['s3'] == combo_row['s2']):
                    # kek.insert(combo_row)

                    results[group_id] += combo_row['value']

                    if commentary:
                        print(f"Found combo: {combo_row['name']}")

                    found_combo = True
                    break

                if (build_row['s1'] == combo_row['s3'] and build_row['s2'] ==
                        combo_row['s3'] and build_row['s3'] == combo_row['s1']):
                    # kek.insert(combo_row)

                    results[group_id] += combo_row['value']

                    if commentary:
                        print(f"Found combo: {combo_row['name']}")

                    found_combo = True
                    break


            if not found_combo:
                for _, df_row in default_values.iterrows():

                    if df_row.s == build_row['s1'] or df_row.s == build_row[
                        's2'] or df_row.s == build_row['s3']:

                        results[group_id] += df_row.value

                        if commentary:
                            print(f"Item {df_row['name']} not in combo")


    for group_id in range(4):
        print(f"{group_name[group_id]}: {results[group_id]}")
