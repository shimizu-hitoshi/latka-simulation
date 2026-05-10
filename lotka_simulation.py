import random


def simulate_lotka(author_total=721, alpha=41):
    """
    著者の論文出版分布をシミュレートする関数。
    author_total: 総著者数 (デフォルト721)
    alpha: 新しい著者が論文を出版する確率(%) (デフォルト41)
    """
    published = [0] * author_total

    papers = []
    npapers = 0
    nauthors = 0

    while nauthors < author_total:
        if random.randint(0, 99) < alpha or npapers == 0:
            new_author = nauthors
            nauthors += 1
        else:
            new_author = random.choice(papers)

        papers.append(new_author)
        npapers += 1
        published[new_author] += 1

    bins = [0] * 12
    for count in published:
        bin_idx = 11 if count > 11 else count
        bins[bin_idx] += 1

    return bins


def run(trials=10, author_total=721, alpha=41):
    """
    シミュレーションを指定回数（デフォルト10回）実行し、平均を出力する関数。
    trials: 試行回数 (デフォルト10)
    author_total: 総著者数 (デフォルト721)
    alpha: 新しい著者が論文を出版する確率(%) (デフォルト41)
    """
    avg_bins = [0] * 12

    for _ in range(trials):
        bins = simulate_lotka(author_total, alpha)
        for i in range(12):
            avg_bins[i] += bins[i]

    print(f"{trials}回のシミュレーションの平均値:")
    for b in range(1, 12):
        label = f"{b}回" if b < 11 else "11回以上"
        print(f"論文を {label} 出版した著者: {round(avg_bins[b] / trials)}人")


if __name__ == "__main__":
    run()
