# lotka-simulation
https://journals.sagepub.com/doi/10.5153/sro.85

## 論文再現実験コード

Gilbert (1997) に基づく Lotka's Law のシミュレーションを実行できます。

各新規論文は、確率 `alpha` で新しい著者に割り当てられ、そうでない場合は既存論文を一様ランダムに1本選び、その論文の著者に割り当てられます。これにより、著者ごとの論文数分布が Zipf 的な裾の重い分布になります。

### 実行方法

```bash
python lotka_simulation.py --output-dir outputs
```

### 出力

- `outputs/baseline.csv`
- `outputs/higher_alpha.csv`
- `outputs/larger_corpus.csv`
- `outputs/summary.json`

各 CSV には以下の列が出力されます。

- `papers`: 著者が持つ論文数
- `authors`: その論文数を持つ著者数
- `share`: 全著者に占める割合

`summary.json` には実験設定と著者分布の要約統計が保存されます。
