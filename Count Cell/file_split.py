import pandas as pd

def data_taking(input_file):
    with open(input_file, "r") as infile:
        lines = infile.readlines()
    
    output_lines = []
    for line in lines:
        columns = line.strip().split("\t")
         
        if len(columns) >= 2:
            output_lines.append("\t".join(columns[:2]))

    with open(input_file, "w") as outfile:
        outfile.write("\n".join(output_lines))

# def split_file_by_lines(input_file, num_files):
#     with open(input_file, "r") as file:
#         lines = file.readlines()
#         lines_per_file = len(lines) // num_files  

#         for i in range(num_files):
#             start = i * lines_per_file
#             end = (i + 1) * lines_per_file
#             with open(f"file{i+1}.txt", "w") as out_file:
#                 out_file.writelines(lines[start:end])


#Tách thành các file nhỏ tại những điểm thời gian gián đoạn
def split_file_by_difference(input_file, output_prefix, k):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    prev_time = None
    current_chunk = []
    chunk_number = 1

    for line in lines:
        try:
            value = line.split()
            time=float(value[0])  
        except ValueError:
            continue  

        if prev_time is None:
            prev_time = time
            current_chunk.append(line)
        else:
            difference = round(time - prev_time,4)
            if difference != k:
                output_file = f"{output_prefix}{chunk_number}.txt"
                with open(output_file, 'w') as out_f:
                    out_f.writelines(current_chunk)
                chunk_number += 1
                current_chunk = [line]
            else:
                current_chunk.append(line)
            prev_time = time

    output_file = f"{output_prefix}_{chunk_number}.txt"
    with open(output_file, 'w') as out_f:
        out_f.writelines(current_chunk)

def column_creating(input_file,reference_time):
    time_column=[]
    value_column=[]
    with open(input_file,'r') as f:
        for line in f:
            p=line.split()
            time_column.append(float(p[0]))
            value_column.append(float(p[1]))

    df = pd.DataFrame({'time': time_column, 'value': value_column})

    df['new_column'] = 0

    df.loc[df['time'].isin(reference_time), 'new_column'] = 2
    df.to_csv(input_file,sep='\t',index=False,header=False,float_format="%.6f")


