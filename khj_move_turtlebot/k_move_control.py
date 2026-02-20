import sys
import rclpy
import time
from rclpy.node import Node
from std_srvs.srv import SetBool
from rclpy.action import ActionClient, ActionServer, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.qos import qos_profile_sensor_data

from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PySide6.QtCore import QThread
from PySide6.QtGui import QColor

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from turtlebot3_msgs.action import Patrol

from .k_move_control_ui import Ui_MainWindow

class RclpyThread(QThread):
    def __init__(self, executor):
        super().__init__()
        self.executor = executor
    def run(self):
        try: self.executor.spin()
        finally: rclpy.shutdown()

# ===============================
# ACTION SERVER (회전 동작 실행)
# ===============================

class Turtlebot3PatrolServer(Node):
    def __init__(self):
        super().__init__('turtlebot3_patrol_server')

        self._action_server = ActionServer(
            self, Patrol, 'turtlebot3',
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def goal_callback(self, goal_request): return GoalResponse.ACCEPT # 목표 수락 여부
    def cancel_callback(self, cancel_request): return CancelResponse.ACCEPT # 목표 수락 여부
    # 실제 동작 실행
    def execute_callback(self, goal_handle):
        msg = Twist()
        msg.angular.z = 0.6
        for count in range(8):
            if goal_handle.is_cancel_requested: break
            for _ in range(15):
                if goal_handle.is_cancel_requested:
                    self.stop_robot()
                    goal_handle.canceled()
                    return Patrol.Result()
                self.cmd_vel_pub.publish(msg)
                time.sleep(0.1)
            self.stop_robot()
            time.sleep(0.2)
        self.stop_robot()
        goal_handle.succeed()
        return Patrol.Result()

    def stop_robot(self):
        self.cmd_vel_pub.publish(Twist())

# ===============================
# MAIN CONTROL NODE (GUI + 통신)
# ===============================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        rclpy.init()
        self.executor = MultiThreadedExecutor()
        self.pub_move = Node('move_turtle')

        # --------- TOPIC Publisher ---------
        # /cmd_vel 로 속도 명령 전송

        self.move_turtle_pub = self.pub_move.create_publisher(Twist, '/cmd_vel', 10)

        # --------- TOPIC Subscriber ---------
        # /scan 라이다 데이터 수신

        self.scan_sub = self.pub_move.create_subscription(
            LaserScan, 'scan', self.scan_callback, qos_profile=qos_profile_sensor_data)

        self.safety_mode = False
        self.is_obstacle_detected = False

        # --------- SERVICE SERVER ---------
        # 안전모드 ON/OFF 요청 처리

        self.safety_service = self.pub_move.create_service(
            SetBool,
            'set_safety_mode',
            self.handle_safety_service
        )
        self._goal_handle = None

        # --------- ACTION CLIENT ---------
        # 장애물 감지 시 회전 요청

        self._action_client = ActionClient(self.pub_move, Patrol, 'turtlebot3')

        # 버튼 연결
        self.ui.btn_go.clicked.connect(self.btn_go_clicked)
        self.ui.btn_back.clicked.connect(self.btn_back_clicked)
        self.ui.btn_right.clicked.connect(self.btn_right_clicked)
        self.ui.btn_left.clicked.connect(self.btn_left_clicked)
        self.ui.btn_stop.clicked.connect(self.btn_stop_clicked)
        self.ui.btn_safety_on.clicked.connect(self.turn_on_safety)
        self.ui.btn_safety_off.clicked.connect(self.turn_off_safety)

        self.timer = self.pub_move.create_timer(0.1, self.turtle_move)
        self.velocity, self.angular = 0.0, 0.0
        self.rclpy_thread = RclpyThread(self.executor)
        self.rclpy_thread.start()
        self.executor.add_node(self.pub_move)

    # 버튼 함수들
    def btn_go_clicked(self):
        if not self.is_obstacle_detected: self.velocity += 0.2

    def btn_back_clicked(self):
        if not self.is_obstacle_detected: self.velocity -= 0.2

    def btn_right_clicked(self):
        if not self.is_obstacle_detected: self.angular -= 0.2

    def btn_left_clicked(self):
        if not self.is_obstacle_detected: self.angular += 0.2

    def btn_stop_clicked(self):
        self.velocity = 0.0
        self.angular = 0.0


        if self._goal_handle is not None:
            self._goal_handle.cancel_goal_async()  # 액션 취소
            self._goal_handle = None
        self.move_turtle_pub.publish(Twist())

    def scan_callback(self, msg):
        ranges = msg.ranges
        num = len(ranges)
        if num == 0: return

        front = [r for r in (ranges[:30] + ranges[-30:]) if r > 0.1]
        back = [r for r in ranges[int(num/2)-30 : int(num/2)+30] if r > 0.1]
        sides = [r for r in (ranges[int(num/4)-30:int(num/4)+30] + ranges[int(num*3/4)-30:int(num*3/4)+30]) if r > 0.1]

        check_list = front + back + sides
        if not check_list: return

        dist = min(check_list)

        if dist < 0.5 and self.safety_mode:
            if not self.is_obstacle_detected:
                self.warn_action(dist)
        elif dist >= 0.8:
            self.is_obstacle_detected = False

    def warn_action(self, dist):
        self.is_obstacle_detected = True
        self.velocity, self.angular = 0.0, 0.0

        item = QListWidgetItem(f"장애물({dist:.2f}m) 감지! 회전 동작")
        item.setForeground(QColor("red")) # [빨강]
        self.ui.listWidget.addItem(item)

        goal = Patrol.Goal()
        self._action_client.wait_for_server()
        self._action_client.send_goal_async(goal, feedback_callback=self.feedback_callback).add_done_callback(self.goal_response_callback)

    # 액션 피드백
    def feedback_callback(self, feedback_msg):
        item = QListWidgetItem(f"{feedback_msg.feedback.state}")
        item.setForeground(QColor("orange")) # [주황]
        self.ui.listWidget.addItem(item)
        self.ui.listWidget.scrollToBottom()

    def goal_response_callback(self, future): self._goal_handle = future.result()

    def handle_safety_service(self, request, response):

        self.safety_mode = request.data

        if self.safety_mode:
            self.turn_on_safety()
            response.message = "안전 모드 활성화"
        else:
            self.turn_off_safety()
            response.message = "안전 모드 비활성화"

        response.success = True
        return response

    def turn_on_safety(self):
        self.safety_mode = True
        item = QListWidgetItem("안전 모드 ON")
        item.setForeground(QColor("blue"))
        self.ui.listWidget.addItem(item)

    def turn_off_safety(self):
        self.safety_mode = False
        self.is_obstacle_detected = False
        self.velocity, self.angular = 0.0, 0.0
        if self._goal_handle: self._goal_handle.cancel_goal_async()
        item = QListWidgetItem("안전 모드 OFF: 주행 가능")
        item.setForeground(QColor("darkgreen"))
        self.ui.listWidget.addItem(item)
        self.ui.listWidget.scrollToBottom()

    def turtle_move(self):
        if self.is_obstacle_detected: return
        msg = Twist()
        msg.linear.x, msg.angular.z = self.velocity, self.angular
        self.move_turtle_pub.publish(msg)
        self.ui.lbl_linear.setText(f"선속도: {self.velocity:.2f}")
        self.ui.lbl_angular.setText(f"각속도: {self.angular:.2f}")

    def closeEvent(self, event):
        self.executor.shutdown(); self.rclpy_thread.quit()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = MainWindow(); server = Turtlebot3PatrolServer()
    window.executor.add_node(server); window.show()
    sys.exit(app.exec())

if __name__ == '__main__': main()


