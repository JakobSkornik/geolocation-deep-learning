import math
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def loader(current, max):
    if current == 0:
        print("[", end="")

    if current % (max / 10) == 0:
        print("#", end="")

    if current == max - 1:
        print("]")


def plot_accuracy(model_history, epochs):
    acc = model_history.history["accuracy"]
    val_acc = model_history.history["val_accuracy"]

    loss = model_history.history["loss"]
    val_loss = model_history.history["val_loss"]

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training Accuracy")
    plt.plot(epochs_range, val_acc, label="Validation Accuracy")
    plt.legend(loc="lower right")
    plt.title("Training and Validation Accuracy")

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Training Loss")
    plt.plot(epochs_range, val_loss, label="Validation Loss")
    plt.legend(loc="upper right")
    plt.title("Training and Validation Loss")
    plt.show()


def plot_ljubljana(points, point_scores, actual, N):
    bounds = (
        14.464685451682861,
        14.543838918732977,
        46.02095210929212,
        46.09861511084722,
    )
    lj = plt.imread("./data/ljubljana/map.png")
    _, ax = plt.subplots(figsize=(8, 7))

    ax.set_title("Map of Ljubljana")
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])

    N = 8

    dx = (bounds[1] - bounds[0]) / 8
    x = dx + bounds[0]
    for _ in range(N - 1):
        ax.axvline(x=x, color="b", alpha=0.3)
        x += dx

    dy = (bounds[3] - bounds[2]) / N
    y = dy + bounds[2]
    for _ in range(N - 1):
        ax.axhline(y=y, color="b", alpha=0.3)
        y += dy

    for i in range(len(points)):
        y = int(points[i]) // 10
        x = int(points[i]) % 10

        rect = patches.Rectangle(
            (bounds[0] + x * dx, bounds[2] + y * dy),
            dx,
            dy,
            linewidth=1,
            edgecolor="r",
            facecolor="r",
            alpha=point_scores[i],
        )

        ax.add_patch(rect)

        rect = patches.Rectangle(
            (bounds[0] + int(actual["class"].split("-")[1]) * dx, bounds[2] + int(actual["class"].split("-")[0]) * dy),
            dx,
            dy,
            linewidth=1,
            edgecolor="b",
            facecolor="b",
            alpha=point_scores[i],
        )
        ax.scatter(float(actual["x"]), float(actual["y"]), c="b", zorder=1, alpha=1, s=5)

        ax.add_patch(rect) 
        ax.text(
            bounds[0] + x * dx + dx / 2,
            bounds[2] + y * dy + dy / 2,
            points[i],
            color="r",
        )

    ax.imshow(lj, zorder=0, extent=bounds, aspect="equal")


def plot_dataset(folder):
    x = []
    y = []
    data_dir = "./data/"
    dataset_dir = os.path.join(data_dir, folder)

    for class_dir in os.listdir(dataset_dir):
        if class_dir[0] == ".":
            continue

        class_dir_path = os.path.join(dataset_dir, class_dir)
        for img in os.listdir(class_dir_path):
            img = img.replace(".png", "").split(",")
            x.append(float(img[0]))
            y.append(float(img[1]))

    # Plot points on the map
    bounds = (
        14.464685451682861,
        14.543838918732977,
        46.02095210929212,
        46.09861511084722,
    )
    lj = plt.imread("./data/ljubljana/map.png")
    _, ax = plt.subplots(figsize=(8, 8))

    ax.set_title(f"Map of Ljubljana with {len(x) // 3} streetviews")
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])

    ax.scatter(y, x, c="r", zorder=1, alpha=0.2, s=5)
    ax.imshow(lj, zorder=0, extent=bounds, aspect="equal")


def plot_point_and_class(point):
    bounds = (
        14.464685451682861,
        14.543838918732977,
        46.02095210929212,
        46.09861511084722,
    )

    N = 8
    x_dif = bounds[1] - bounds[0]
    y_dif = bounds[3] - bounds[2]
    x_width = x_dif / N
    y_width = y_dif / N

    def class_mapper(label):
        coords = label.split(",")
        lat = float(coords[0])
        lng = float(coords[1])
        lat = math.floor((lat - bounds[2]) / x_width)
        lng = math.floor((lng - bounds[0]) / y_width)
        return f"{lat}-{lng}"

    label = class_mapper(point)
    lj = plt.imread("./data/ljubljana/map.png")
    _, ax = plt.subplots(figsize=(8, 8))

    ax.set_title(f"Map of Ljubljana with point {point} and label {label}")
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])

    x, y, _ = point.split(",")
    x_str, y_str = label.split("-")
    x_c = int(x_str)
    y_c = int(y_str)

    rect = patches.Rectangle(
        (bounds[0] + y_c * y_width, bounds[2] + x_c * x_width),
        y_width,
        x_width,
        linewidth=1,
        edgecolor="r",
        facecolor="none",
    )
    ax.add_patch(rect)

    ax.scatter([float(y)], [float(x)], c="r", zorder=1, alpha=1, s=15)
    ax.imshow(lj, zorder=0, extent=bounds, aspect="equal")
