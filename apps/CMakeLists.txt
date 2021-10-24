add_executable(app_main app_main.cpp)
target_compile_features(app_main PRIVATE cxx_std_17)

target_link_libraries(app_main PRIVATE mylib)
