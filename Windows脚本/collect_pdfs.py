from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DEFAULT_SOURCE = Path(r"C:\Users\cjy\Desktop\现实数据驱动微调")
DEFAULT_OUTPUT = Path("output")


def build_flat_filename(source_dir: Path, pdf_path: Path) -> str:
    relative_path = pdf_path.relative_to(source_dir)
    # flat_name = "__".join(relative_path.parts) # 将路径中的分隔符替换为双下划线，避免文件名冲突
    flat_name = relative_path.parts[-1]  # 只保留文件名部分，忽略目录结构
    return flat_name


def collect_pdfs(source_dir: Path, output_dir: Path) -> int:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for pdf_path in source_dir.rglob("*"):
        if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
            continue

        destination_path = output_dir / build_flat_filename(source_dir, pdf_path)
        shutil.copy2(pdf_path, destination_path)
        copied += 1

    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="递归收集 PDF 文件到输出目录")
    parser.add_argument("source", nargs="?", default=str(DEFAULT_SOURCE), help="要搜索的源目录")
    parser.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT), help="输出目录，默认是 ./output")
    args = parser.parse_args()

    copied = collect_pdfs(Path(args.source), Path(args.output))
    print(f"已复制 {copied} 个 PDF 文件到 {Path(args.output).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())