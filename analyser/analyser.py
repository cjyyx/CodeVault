import time
from collections import defaultdict


class CodeTimer:
    """
    一个用于测量代码段执行耗时的计时器
    """

    def __init__(self) -> None:
        self.data = defaultdict(list)
        self.start_of_block = None
        self.last_point_time = None

    def reset(self) -> None:
        """重置单个时间点的计时起点。不清空已记录的数据。"""
        self.last_point_time = time.time()

    def clear(self) -> None:
        """清空所有已记录的性能数据。"""
        self.data.clear()

    def point(self, label: str) -> None:
        """
        记录一个时间点。
        计算从上一个 reset() 或 point() 到现在的时间差，并与标签 label 关联。
        """
        if self.last_point_time is None:
            self.reset()
            # 如果这是第一次调用 point，我们不记录从 with 开始到此的时间，
            # 因为这部分时间的标签是未知的。后续的 point 才有意义。
            return

        current_time = time.time()
        duration = current_time - self.last_point_time
        self.data[label].append(duration)
        self.last_point_time = current_time

    def report(self) -> None:
        """打印性能分析报告。"""
        if self.start_of_block is None:
            print("计时器从未使用过 (请使用 'with CodeTimer() as timer:' 模式)。")
            return

        total_wall_time = time.time() - self.start_of_block
        print(f"总分析时长 (Wall Time): {total_wall_time:.4f} 秒")

        if not self.data:
            print("警告：没有记录任何时间点 (没有调用 timer.point())。")
            return

        total_recorded_time = sum(sum(durations) for durations in self.data.values())
        print(f"所有已记录任务总耗时: {total_recorded_time:.4f} 秒\n")

        # 按总耗时降序排序，使报告更具可读性
        sorted_data = sorted(self.data.items(), key=lambda item: sum(item[1]), reverse=True)

        for label, durations in sorted_data:
            if not durations:
                continue

            count = len(durations)
            total_time = sum(durations)
            mean_time = total_time / count
            percentage = (100 * total_time / total_recorded_time) if total_recorded_time > 0 else 0

            print(f"任务: {label}")
            print(f"  - 触发次数: {count}")
            print(f"  - 总耗时: {total_time:.4f} 秒")
            print(f"  - 平均耗时: {mean_time:.4f} 秒")
            print(f"  - 在已记录任务中占比: {percentage:.2f}%")
            print("-" * 30)

    def __enter__(self):
        """上下文管理器入口，开始计时。"""
        self.start_of_block = time.time()
        self.last_point_time = self.start_of_block  # 将第一个计时的起点设为 with 语句的开始
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口，自动打印报告。"""
        self.report()


# 使用示例
if __name__ == "__main__":
    print("--- 使用上下文管理器 ---")
    with CodeTimer() as timer:
        time.sleep(0.1)
        timer.point("数据加载")

        time.sleep(0.3)

        timer.point("模型预处理")

    print("\n--- 手动使用 ---")
    timer = CodeTimer()
    timer.__enter__()  # 手动模拟进入
    timer.reset()
    time.sleep(0.2)
    timer.point("任务A")
    timer.report()  # 手动打印
