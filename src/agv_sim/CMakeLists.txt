cmake_minimum_required(VERSION 3.8)
project(agv_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# --- PHẦN THÊM VÀO BẮT ĐẦU TẠI ĐÂY ---
# Lệnh này copy các thư mục tài nguyên vào thư mục 'install' để ROS 2 có thể tìm thấy khi chạy
install(DIRECTORY
  launch
  urdf
  meshes
  config
  worlds
  DESTINATION share/${PROJECT_NAME}
)
# --- PHẦN THÊM VÀO KẾT THÚC TẠI ĐÂY ---

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()