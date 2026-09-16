#include "benchmark.h"
#include "esp_log.h"
#include "esp_spiffs.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
static const char* TAG="app";
extern "C" void app_main(){
 esp_vfs_spiffs_conf_t conf={.base_path="/spiffs",.partition_label="storage",.max_files=8,.format_if_mount_failed=false};
 ESP_ERROR_CHECK(esp_vfs_spiffs_register(&conf)); size_t total=0,used=0;esp_spiffs_info("storage",&total,&used);ESP_LOGI(TAG,"SPIFFS %u/%u bytes",(unsigned)used,(unsigned)total);
 // Place a Voxserv file in firmware/esp32s3/storage before building the SPIFFS image.
 run_benchmark("/spiffs/sample.wav"); vTaskDelete(nullptr);
}
