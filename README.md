# KonoSuba Quartet Codex Pets

《为美好的世界献上祝福！》四人组的非官方 Codex 桌面宠物：阿库娅、惠惠、Kazuma 和真、达克妮丝。

![四人组待机预览](previews/lineup.png)

每只宠物都包含九种标准动作和完整 16 向视线动画，使用透明的 Codex Pets v2 精灵图格式。四张成品均已通过 Codex Pets 结构预检。

> 这是粉丝制作的同人项目，不是官方发布，也不代表或获得原作权利人的认可。

## 宠物

| 预览 | 角色 | 定位 | 安装目录 | 稳定 ID |
| --- | --- | --- | --- | --- |
| <img src="previews/aqua-idle.png" width="96" alt="阿库娅"> | 阿库娅 | 水之女神 | [`pets/aqua/`](pets/aqua/) | `pet_6adad37d859481918b29a99e2d388ccc` |
| <img src="previews/megumin-idle.png" width="96" alt="惠惠"> | 惠惠 | 红魔族大魔法师 | [`pets/megumin/`](pets/megumin/) | `pet_6adac38a8d28819191f5db9c38f5c71c` |
| <img src="previews/kazuma-idle.png" width="96" alt="Kazuma 和真"> | Kazuma 和真 | 冒险者 | [`pets/kazuma/`](pets/kazuma/) | `pet_6ad9e8f1524481919994224aa8b56e8f` |
| <img src="previews/darkness-idle.png" width="96" alt="达克妮丝"> | 达克妮丝 | 十字骑士 | [`pets/darkness/`](pets/darkness/) | `pet_6adaf9cdca788191a52e4d5d03ba4a5a` |

## 安装

### macOS / Linux

```bash
git clone https://github.com/zjsycwmrbig/KonoSuba-Quartet-Codex-Pets.git
mkdir -p "$HOME/.codex/pets"
cp -R KonoSuba-Quartet-Codex-Pets/pets/* "$HOME/.codex/pets/"
```

### Windows PowerShell

```powershell
git clone https://github.com/zjsycwmrbig/KonoSuba-Quartet-Codex-Pets.git
$pets = Join-Path $HOME ".codex\pets"
New-Item -ItemType Directory -Force $pets | Out-Null
Copy-Item -Recurse -Force ".\KonoSuba-Quartet-Codex-Pets\pets\*" $pets
```

完成复制后，重新打开 Codex 的宠物选择器即可看到这四个宠物包。

## 预览

| 角色 | 动作总览 | 16 向 QA | 接触表 |
| --- | --- | --- | --- |
| 阿库娅 | [动作 GIF](previews/aqua-all-states.gif) | [方向图](previews/aqua-look-directions.png) | [接触表](previews/aqua-contact.png) |
| 惠惠 | [动作 GIF](previews/megumin-all-states.gif) | [方向图](previews/megumin-look-directions.png) | [接触表](previews/megumin-contact.png) |
| Kazuma 和真 | [动作 GIF](previews/kazuma-all-states.gif) | [方向图](previews/kazuma-look-directions.png) | [接触表](previews/kazuma-contact.png) |
| 达克妮丝 | [动作 GIF](previews/darkness-all-states.gif) | [方向图](previews/darkness-look-directions.png) | [接触表](previews/darkness-contact.png) |

`previews/` 还包含每只宠物的待机、左右移动、挥手、跳跃、失败、等待、工作、检查、视线环和 `idle → jump → idle` 闭环预览。

## 精灵图规格

- 格式：Codex Pets v2
- 尺寸：`1536 × 2288`
- 单元格：`192 × 208`
- 网格：`8 × 11`
- 标准动作：九行，共 57 帧
- 视线方向：两行，共 16 帧
- 安装素材：透明无损 WebP
- PNG 母版：`assets/spritesheets/`

每行帧数：

```text
idle               6
running-right      8
running-left       8
waving             4
jumping            5
failed             8
waiting            6
running            6
review             6
look 000–157.5     8
look 180–337.5     8
```

## 校验

仓库自带独立的 Pillow 结构校验脚本：

```bash
python3 -m pip install Pillow
python3 scripts/validate_repo.py
```

它会检查尺寸、网格、必需帧、未使用单元格透明性、PNG/WebP 像素一致性、清单引用和 SHA-256。GitHub Actions 会在每次推送和拉取请求时运行同一套检查。

官方 Codex Pets 预检结果与素材哈希记录在 [docs/VALIDATION.md](docs/VALIDATION.md)，完整机器可读信息位于 [manifest.json](manifest.json)。

## 目录

```text
pets/<slug>/
├── pet.json
└── spritesheet.webp

assets/spritesheets/<slug>.png    # 原始 PNG 母版
previews/                         # 动作与方向预览
scripts/validate_repo.py          # 独立校验器
manifest.json                     # 角色、规格与哈希清单
SHA256SUMS                        # 全部发布文件校验和
```

## English

KonoSuba Quartet Codex Pets is a set of four unofficial fan-made desktop pets
for Codex: Aqua, Megumin, Kazuma Satou, and Darkness. Each self-contained pack
contains a `pet.json` and a transparent, lossless WebP sprite sheet in the
Codex Pets v2 format (`1536 × 2288`, `8 × 11` grid, 73 frames).

Copy the contents of `pets/` to `~/.codex/pets` on macOS/Linux or
`%USERPROFILE%\.codex\pets` on Windows, then reopen the Codex pet picker.
Run `python3 scripts/validate_repo.py` to verify the repository.

## 许可与声明

- 仓库中的文档、配置和校验代码使用 [MIT License](LICENSE)。
- 创作者对粉丝绘制宠物素材的原创贡献按 [CC BY 4.0](LICENSE-ASSETS) 提供。
- 《为美好的世界献上祝福！》及相关角色、名称与设定的权利归其各自权利人所有。
- 上述素材许可不授予任何第三方角色、商标或原作权利。详见 [NOTICE.md](NOTICE.md)。

维护者：[@zjsycwmrbig](https://github.com/zjsycwmrbig)
