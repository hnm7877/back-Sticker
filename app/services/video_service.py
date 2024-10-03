import moviepy.editor as mp

def apply_watermark_to_video(video_path, watermark_path, position, size):
    video_clip = mp.VideoFileClip(video_path)
    watermark = (mp.ImageClip(watermark_path)
                  .set_duration(video_clip.duration)
                  .resize(size)
                  .set_position(position)
                  .set_opacity(0.5))
    
    final_clip = mp.CompositeVideoClip([video_clip, watermark])
    
    output_path = "temp/output_video.mp4"
    final_clip.write_videofile(output_path)
    return output_path
