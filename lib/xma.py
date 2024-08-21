import subprocess
import os

def export_xma(input_file_path, output_file_path):
	try:
		## vgmstream
		subprocess.run(['vgmstream-cli', input_file_path, '-o', output_file_path], check=True)
		
		## FFmpeg
		#subprocess.run(['ffmpeg', '-i', input_file_path, '-acodec', 'pcm_s16le', '-ar', '44100', output_file_path], check=True)
		
		print(f"Conversion successful: {output_file_path}")
	except subprocess.CalledProcessError as e:
		print(f"Error during conversion: {e}")