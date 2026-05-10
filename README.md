# latka-simulation
https://journals.sagepub.com/doi/10.5153/sro.85

## 論文再現実験コード

Lotka-Volterra（被食者-捕食者）モデルで、論文再現用の実験を実行できます。

### 実行方法

```bash
python lotka_simulation.py --output-dir outputs
```

### 出力

- `outputs/baseline.csv`
- `outputs/high_initial_prey.csv`
- `outputs/low_initial_predator.csv`
- `outputs/summary.json`

`summary.json` には実験設定と最終結果（最大値・最終値）が保存されます。
