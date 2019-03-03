<template>
    <v-layout overflow-hidden column align-center style="background-color:black;height:100%;padding-bottom:56px" full-height justify-center>
        <div class="headline text-xs-center">
            <vue-cropper
                ref="cropper"
                :src="cropImage"
                alt="Source Image"
                :aspectRatio="0.6875"
                :guides="true"
                :view-mode="1"
                drag-mode="crop"
                :auto-crop-area="0.5"
                :background="false"
                :rotatable="true"
                :minContainerWidth="300"
                :minContainerHeight="300"
                >
                
            </vue-cropper>
        </div>
        <v-bottom-nav
        :value="true"
        absolute
        app
        >
            <v-btn @click="cancel">
                <v-icon >cancel</v-icon>
            </v-btn>

            <v-btn @click="rotate">
                <v-icon >crop_rotate</v-icon>
            </v-btn>

            <v-btn @click="crop">
                <v-icon >save</v-icon>
            </v-btn>
        </v-bottom-nav>
    </v-layout>
</template>
<script>
    import VueCropper from 'vue-cropperjs';
    require('vue-cropperjs')
    export default {
      components: {
        VueCropper
      },
      data() {
        return {
          windowSize: {
            x: 0,
            y: 0
          },
          currentImage: String,
          finishImage: String,
        }
      },
      props: {
        cropImage: String
      },
      methods: {
        cancel() {
          this.$emit('close')
        },
        rotate() {
          this.$refs.cropper.rotate(90);
        },
        crop() {
          const photoUrl = this.$refs.cropper.getCroppedCanvas({

            minWidth: 256,
            minHeight: 256,
            maxWidth: 4096,
            maxHeight: 4096,
            fillColor: '#fff',
            imageSmoothingEnabled: false,
            imageSmoothingQuality: 'high',
          }).toDataURL()
          this.$refs.cropper.getCroppedCanvas({

            minWidth: 256,
            minHeight: 256,
            maxWidth: 4096,
            maxHeight: 4096,
            fillColor: '#fff',
            imageSmoothingEnabled: false,
            imageSmoothingQuality: 'high',
          }).toBlob(blob => {            
            this.$store.commit('photo/setPhotoBlob', blob)
          })
          this.$store.commit('photo/setPhoto', photoUrl)
          this.$store.commit('photo/setBrowserStatus')
          this.$emit('finish')
        }
      },
      mounted() {
        this.currentImage = this.cropImage
      },
      watch: {
        cropImage(cur) {
          this.currentImage = cur
          this.$refs.cropper.replace(cur)
        }
      }
    }
</script>