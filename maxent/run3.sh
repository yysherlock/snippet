python trainer.py detector.model3 -f data/train_data.txt -g 0.02 --iters 15
python predictor.py -m detector.model3 -i data/train_data.txt -o result3
#python predictor.py -m detector.model1 -i data/train/t900.txt -o result1
python evaluator.py -p result3 -s data/train_data.txt
#python evaluator.py -a result1 -s data/train/t900.txt
