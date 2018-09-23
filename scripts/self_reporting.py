import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def plot(scores, plot_name):

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)

    ax = sns.boxplot(data=scores, x = 'System', y='MOS', hue="Self-Report")
    ax.set(xlabel='System', ylabel='Mean-Opinion Self-Report Scores')
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

    ax.set_xlabel("Systems", fontsize=30)
    ax.set_ylabel("Self-report ratings", fontsize=30)
    ax.tick_params(labelsize=25)


    leg_handles = ax.get_legend_handles_labels()[0]

    ax.legend( leg_handles, ['Naturalness','Cognitive Load', 'Motivation',],bbox_to_anchor=(1.05, 1),loc=2, borderaxespad=0.,  markerscale=5)

    plt.setp(ax.get_legend().get_texts(), fontsize='25') # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize='18') # for legend title

    ax.figure.savefig(plot_name, bbox_inches="tight")

    return 0

if __name__ == '__main__':

    #print(sys.argv)
    csv_filepath = sys.argv[1]
    systems_map_file = sys.argv[2]
    plot_path = sys.argv[3]
    csvDir=sys.argv[4]

    self_report = pd.read_csv(csv_filepath)
    scores = self_report.melt(id_vars=['Subject','System'], value_vars=['Naturalness','Cognitive_Load','Motivation'])
    scores.rename(columns={'variable': 'Self-Report', 'value': 'MOS'}, inplace=True)

    if systems_map_file != None:
        with open(systems_map_file, 'r') as ids:
            system_ids = ids.readlines()
            system_ids = [y.strip() for y in system_ids]

        for system in system_ids:
            info = system.split(":")
            scores['System'].replace(info[0], info[1], inplace=True)

    plot_name = plot_path +"/"+"self_report.pdf"

    plot(scores,plot_name)
    print("Saving updated self-report data as CSV ....")
    csv_name = csvDir+"/"+"self_report.csv"
    scores.to_csv(csv_name, encoding='utf-8', index=False)
