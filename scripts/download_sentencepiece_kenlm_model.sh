OUTPUT_DIR="./models"
if [ ! -d OUTPUT_DIR ]
then
  mkdir $OUTPUT_DIR
fi
echo "Downloading Vietnamese Sentencepiece model to $OUTPUT_DIR"
wget https://huggingface.co/edugp/kenlm/resolve/main/wikipedia/vi.sp.model -P $OUTPUT_DIR

echo "Downloading Vietnamese KenLM model to $OUTPUT_DIR"
wget https://huggingface.co/edugp/kenlm/resolve/main/wikipedia/vi.arpa.bin -P $OUTPUT_DIR