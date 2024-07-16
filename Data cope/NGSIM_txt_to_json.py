import pandas as pd
import json
from collections import defaultdict

# 定义输入和输出文件名
input_file = 'trajectories-0515-0530.txt'
output_file = 'trajectories-0515-0530.json'

# 定义一个函数来写入JSON文件
def write_to_json(data, filename):
    with open(filename, 'a') as json_file:
        json_str = json.dumps(data, ensure_ascii=False)  # 将数据转换为JSON字符串
        json_file.write(json_str + '\n')  # 写入JSON字符串并换行

def process_data(input_file, output_file):
    # 使用0到17作为列名，列名包括车辆ID和其他数据
    column_names = [
        'vehicle_id', 'frame_id', 'total_frames', 'timestamp', 'local_x', 'local_y', 
        'global_x', 'global_y', 'v_length', 'v_width', 'v_class', 'v_vel', 
        'v_acc', 'lane_id', 'preceding', 'following', 'space_headway', 'time_headway'
    ]

    # 读取数据文件并打印前几行数据进行验证
    data = pd.read_csv(input_file, delim_whitespace=True, names=column_names, dtype={
        'vehicle_id': int,
        'frame_id': int,
        'total_frames': int,
        'timestamp': 'Int64',
        'local_x': float,
        'local_y': float,
        'global_x': float,
        'global_y': float,
        'v_length': float,
        'v_width': float,
        'v_class': int,
        'v_vel': float,
        'v_acc': float,
        'lane_id': int,
        'preceding': int,
        'following': int,
        'space_headway': float,
        'time_headway': float
    })
    print("数据前5行:")
    print(data.head())  # 打印前5行数据以检查是否正确读取

    current_vehicle_id = None
    result = defaultdict(lambda: defaultdict(list))
    vehicle_count = 0

    # 遍历数据行，整理成需要的格式
    for index, row in data.iterrows():
        vehicle_id = row['vehicle_id']
        
        # 每次遇到新的Vehicle_ID时，保存之前的数据
        if current_vehicle_id is not None and vehicle_id != current_vehicle_id:
            vehicle_data = {
                'vehicle_id': int(current_vehicle_id),
                'total_frames': int(result[current_vehicle_id]['total_frames'][0]),
                'v_class': int(result[current_vehicle_id]['v_class'][0]),
                'v_length': float(result[current_vehicle_id]['v_length'][0]),
                'v_width': float(result[current_vehicle_id]['v_width'][0]),
                'frame_id': [int(x) for x in result[current_vehicle_id]['frame_id']],
                'timestamp': [int(x) for x in result[current_vehicle_id]['timestamp']],
                'local_x': [float(x) for x in result[current_vehicle_id]['local_x']],
                'local_y': [float(x) for x in result[current_vehicle_id]['local_y']],
                'global_x': [float(x) for x in result[current_vehicle_id]['global_x']],
                'global_y': [float(x) for x in result[current_vehicle_id]['global_y']],
                'v_vel': [float(x) for x in result[current_vehicle_id]['v_vel']],
                'v_acc': [float(x) for x in result[current_vehicle_id]['v_acc']],
                'lane_id': [int(x) for x in result[current_vehicle_id]['lane_id']],
                'preceding': [int(x) for x in result[current_vehicle_id]['preceding']],
                'following': [int(x) for x in result[current_vehicle_id]['following']],
                'space_headway': [float(x) for x in result[current_vehicle_id]['space_headway']],
                'time_headway': [float(x) for x in result[current_vehicle_id]['time_headway']]
            }
            write_to_json(vehicle_data, output_file)
            result = defaultdict(lambda: defaultdict(list))
            vehicle_count += 1
            if vehicle_count % 200 == 0:
                print(f'已处理{vehicle_count}辆车的数据')
        
        current_vehicle_id = vehicle_id

        # Append多值属性
        result[vehicle_id]['frame_id'].append(row['frame_id'])
        result[vehicle_id]['timestamp'].append(row['timestamp'])
        result[vehicle_id]['local_x'].append(row['local_x'])
        result[vehicle_id]['local_y'].append(row['local_y'])
        result[vehicle_id]['global_x'].append(row['global_x'])
        result[vehicle_id]['global_y'].append(row['global_y'])
        result[vehicle_id]['v_vel'].append(row['v_vel'])
        result[vehicle_id]['v_acc'].append(row['v_acc'])
        result[vehicle_id]['lane_id'].append(row['lane_id'])
        result[vehicle_id]['preceding'].append(row['preceding'])
        result[vehicle_id]['following'].append(row['following'])
        result[vehicle_id]['space_headway'].append(row['space_headway'])
        result[vehicle_id]['time_headway'].append(row['time_headway'])

        # 直接赋值不变属性
        result[vehicle_id]['total_frames'] = [row['total_frames']]
        result[vehicle_id]['v_class'] = [row['v_class']]
        result[vehicle_id]['v_length'] = [row['v_length']]
        result[vehicle_id]['v_width'] = [row['v_width']]

    # 保存最后一个Vehicle_ID的数据
    if current_vehicle_id is not None:
        vehicle_data = {
            'vehicle_id': int(current_vehicle_id),
            'total_frames': int(result[current_vehicle_id]['total_frames'][0]),
            'v_class': int(result[current_vehicle_id]['v_class'][0]),
            'v_length': float(result[current_vehicle_id]['v_length'][0]),
            'v_width': float(result[current_vehicle_id]['v_width'][0]),
            'frame_id': [int(x) for x in result[current_vehicle_id]['frame_id']],
            'timestamp': [int(x) for x in result[current_vehicle_id]['timestamp']],
            'local_x': [float(x) for x in result[current_vehicle_id]['local_x']],
            'local_y': [float(x) for x in result[current_vehicle_id]['local_y']],
            'global_x': [float(x) for x in result[current_vehicle_id]['global_x']],
            'global_y': [float(x) for x in result[current_vehicle_id]['global_y']],
            'v_vel': [float(x) for x in result[current_vehicle_id]['v_vel']],
            'v_acc': [float(x) for x in result[current_vehicle_id]['v_acc']],
            'lane_id': [int(x) for x in result[current_vehicle_id]['lane_id']],
            'preceding': [int(x) for x in result[current_vehicle_id]['preceding']],
            'following': [int(x) for x in result[current_vehicle_id]['following']],
            'space_headway': [float(x) for x in result[current_vehicle_id]['space_headway']],
            'time_headway': [float(x) for x in result[current_vehicle_id]['time_headway']]
        }
        write_to_json(vehicle_data, output_file)
        vehicle_count += 1

    print(f'已处理{vehicle_count}辆车的数据')
    print('所有数据处理完成')

# 调用处理函数
process_data(input_file, output_file)
