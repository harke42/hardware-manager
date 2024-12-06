from io import BytesIO
from flask import Response, Flask, render_template
import threading
import time
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Agg')

class ImageServer:

    def __init__(self, port=5000):
        # Shared data for streams and plots
        self.frame = None
        self.plot_frame = None
        self.frame_data = [None] * 6
        self.plot_data = [[1, 2, 3], [4, 1, 4], [2, 2, 5], [0, 2, 7], [5, 7, 2], [5, 2, 7]]
        self.port = port

        # Threads for updating data, plot, and running Flask
        self.update_data_thread = threading.Thread(target=self.__update_data)
        self.update_plot_thread = threading.Thread(target=self.__plot_points_with_radius)
        self.flask_thread = threading.Thread(target=self.__flask)

    def start(self):
        self.update_data_thread.start()
        self.update_plot_thread.start()
        self.flask_thread.start()

    def __update_data(self):
        pic_path = "/home/harke/Pictures/Screenshots/Screenshot_20241028_110035.png"
        pic = cv2.imread(pic_path)
        frame0 = cv2.hconcat([pic,pic,pic])
        frame0 = cv2.vconcat([frame0,frame0])
        ret, buffer = cv2.imencode('.jpg', frame0)
        print(buffer.shape)
        buffer = buffer.tobytes()
        j = 0
        
        while True:
            frame = None
            #for i in range(len(self.frame_data)):
            #    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            #    cv2.putText(dummy_frame, f"Stream {i + 1}", (50, 50), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            #            
            #    _, encoded_frame = cv2.imencode('.jpg', dummy_frame)
#
            #    if j % 2 == 0:
            #        self.frame_data[i] = encoded_frame.tobytes()
            #    else:
            #        self.frame_data[i] = buffer

            dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(dummy_frame, f"Stream { 1}", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            frame1 = cv2.hconcat([dummy_frame, dummy_frame, dummy_frame])
            frame1 = cv2.vconcat([frame1, frame1])
            _, encoded_frame = cv2.imencode('.jpg', frame1)
            
            if j % 2 == 0:
                self.frame = encoded_frame.tobytes()
            else:
                self.frame = buffer

            j += 1

            # Simulate plot data changes
            self.plot_data = [[np.random.randint(10), np.random.randint(10), np.random.randint(5)] for _ in range(6)]
            time.sleep(1)

    def __plot_points_with_radius(self):
        while True:
            # Generate plot
            fig, ax = plt.subplots()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_aspect('equal', adjustable='box')

            colors = plt.get_cmap('tab10', len(self.plot_data))

            for i, (x, y, radius) in enumerate(self.plot_data):
                circle = plt.Circle((x, y), radius, color=colors(i), alpha=0.3)
                ax.add_patch(circle)
                ax.plot(x, y, 'o', color=colors(i), label=f'Point {i + 1}')

            # Save plot to memory
            buf = BytesIO()
            plt.savefig(buf, format='jpeg')
            buf.seek(0)
            self.plot_frame = buf.read()
            buf.close()
            plt.close(fig)

            time.sleep(1)

    def __flask(self):
        app = Flask(__name__)

        def send_frames(stream_id):
            while True:
                if self.frame is not None:
                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')
                time.sleep(1)

        def send_frames_plot():
            while True:
                if self.plot_frame is not None:
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + self.plot_frame + b'\r\n')
                time.sleep(1)

        @app.route('/')
        def index():
            return render_template('index2.html')

        @app.route('/video_feed_<int:stream_id>')
        def video_feed(stream_id):
            return Response(send_frames(stream_id - 1), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/video_feed_plot')
        def video_feed_plot():
            return Response(send_frames_plot(), mimetype='multipart/x-mixed-replace; boundary=frame')


        app.run(debug=False, threaded=True, host='0.0.0.0', port=self.port)

if __name__ == '__main__':
    ims = ImageServer()
    ims.start()
