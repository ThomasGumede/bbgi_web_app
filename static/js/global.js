const slider = () => {
  const swiperElement = document.querySelector(".swiper");
  if (swiperElement) {
    // swiper slider
    var swiper = new Swiper(".primary-slider", {
      slidesPerView: 1,
      effect: "fade",
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    // hero2  slider
    var swiperThumbs = new Swiper(".hero-slider2-tumbs_slider", {
      loop: true,
      spaceBetween: 10,
      slidesPerView: 3,
      speed: 800,

      // freeMode: true,
      watchSlidesProgress: true,
      breakpoints: {
        1600: {
          spaceBetween: 20,
        },
      },
    });
    var swiper1 = new Swiper(".hero-slider2", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },

      thumbs: {
        swiper: swiperThumbs,
      },
    });

    // featured apartments slider
    var swiper = new Swiper(".featured-apartments-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
        1800: {
          slidesPerView: 4,
        },
      },
    });

    // featured apartments slider2
    var swiper = new Swiper(".featured-apartments-slider2", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
    // testimonials slider
    var swiper = new Swiper(".testimonials-slider", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
    // testimonials2 slider
    var swiper = new Swiper(".testimonials-slider2", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
        },
      },
    });
    // testimonials 3 slider
    const testimonials3ThumbsSlider = new Swiper(
      ".testimonials3-tumbs_slider",
      {
        slidesPerView: "auto",
        cssMode: true,
        preventClicks: false,
      }
    );
    const testimonialsSlider3 = new Swiper(".testimonials-slider-3", {
      slidesPerView: 1,
      loop: true,
      speed: 1500,
      effect: "fade",

      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },

      thumbs: {
        swiper: testimonials3ThumbsSlider,
      },
    });
    // testimonials 4 slider
    var testimonialsSlider4 = new Swiper(".testimonials-slider-4", {
      slidesPerView: 1,
      loop: true,
      speed: 800,

      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
      },
    });

    const testimonialQuoteMenus = document.querySelectorAll(
      ".testimonial-quote-menu"
    );
    // random thumb menu

    if (testimonialQuoteMenus?.length) {
      testimonialQuoteMenus.forEach((quoteMenu, idx) => {
        const menuContainer = quoteMenu.closest(
          ".testimonial-quote-menu-container"
        );

        const quoteMenu2 = quoteMenu;
        let innerHtmlogQuoteMenu2 = "";
        let ul = document.createElement("ul");

        ul.classList.add("testimonial-quote-menu", "testimonial-quote-menu2");

        quoteMenu2.querySelectorAll("li").forEach((li2) => {
          innerHtmlogQuoteMenu2 += `<li>${li2.innerHTML}</li>`;
        });
        ul.innerHTML = innerHtmlogQuoteMenu2;
        if (menuContainer) {
          menuContainer.appendChild(ul);
        }
      });
      const menuCopy = document.querySelector(".testimonial-quote-menu2");

      // add active class to animatable image
      const isActive = (cs) => {
        menuCopy.style.zIndex = 20;
        menuCopy.querySelectorAll("li").forEach((li, idx) => {
          li.classList.remove("active");
          if (cs === idx) {
            li.classList.add("active");
          }

          setTimeout(() => {
            li.classList.remove("active");
            menuCopy.style.zIndex = 1;
          }, 300);
        });
      };

      testimonialsSlider3.eventsListeners.activeIndexChange[0] = (e) => {
        if (
          testimonialsSlider3.realIndex !==
          testimonialsSlider3.previousRealIndex
        ) {
          isActive(testimonialsSlider3.realIndex);
        }
      };
    }

    // news slider
    var swiper = new Swiper(".news-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
      },
    });
    // news single slider
    var swiper = new Swiper(".news-single-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    });

    // properties slider
    var swiper = new Swiper(".properties-slider", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
    // upcoming projects slider
    var swiper = new Swiper(".project-slider-container", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });
    // neighbour slider
    var neighbourswiperThumbs = new Swiper(".neighbour-slider-tumbs_slider", {
      loop: true,
      spaceBetween: 8,
      slidesPerView: 3,
      freeMode: true,
      watchSlidesProgress: true,
    });
    var swiper = new Swiper(".neighbour-slider", {
      slidesPerView: 1,
      speed: 800,

      effect: "fade",
      thumbs: {
        swiper: neighbourswiperThumbs,
      },
    });
    // brands slider
    var swiper = new Swiper(".brand-slider", {
      slidesPerView: 2,
      spaceBetween: 30,
      speed: 800,
      loop: true,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      breakpoints: {
        576: {
          slidesPerView: 3,
        },
        768: {
          slidesPerView: 4,
        },
        992: {
          slidesPerView: 5,
        },
      },
    });

    // portfolio slider
    var swiper = new Swiper(".portfolio-slider", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
        1200: {
          slidesPerView: 4,
        },
      },
    });
    // popular properties slider
    var swiper = new Swiper(".popular-properties-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      autoplay: {
        delay: 5000,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });
    // product details slider
    var swiper = new Swiper(".product-details-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      preventClicksPropagation: false,
      centeredSlides: true,
      autoplay: {
        delay: 10000,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        768: {
          slidesPerView: 1.6,
        },
        992: {
          slidesPerView: 1.55,
        },

        1600: {
          slidesPerView: 1.9,
        },
      },
    });
  }
};

const modal = () => {
  const modalContainers = document.querySelectorAll(".modal-container");

  if (!modalContainers.length) {
    return;
  }

  modalContainers.forEach((modalContainer) => {
    const body = document.body;
    const bodyStyle = body.style;
    const modals = modalContainer.querySelectorAll(".modal");

    modals?.forEach((modal, idx) => {
      const modalOpens = modalContainer.querySelectorAll(
        `[data-modal-index="${idx + 1}"]`
      );

      const modalContent = modal.querySelector(".modal-content");
      const modalCloses = modal.querySelectorAll(".modal-close");
      //  open modal
      modalOpens.forEach((modalOpen) => {
        modalOpen.addEventListener("click", () => {
          modal.style.display = "block";
          bodyStyle.overflow = "hidden";
          bodyStyle.paddingRight = "17px";

          setTimeout(() => {
            // uncomment if you need  body to be scroll down with modal open
            // window.scroll({ top: window.scrollY - 100, behavior: "smooth" });
            modal.style.opacity = 100;
            modal.style.visibility = "visible";
            modal.scrollTop = 0;
            modalContent.style.transform = "translateY(0px)";
          }, 10);
        });
      });
      //  close modal
      modalCloses.forEach((modalClose) => {
        modalClose.addEventListener("click", function () {
          modal.style.opacity = 0;
          modal.style.visibility = "hidden";
          modalContent.style.transform = `translateY(-${80}px)`;

          setTimeout(() => {
            modal.style.display = "none";
            bodyStyle.overflow = "auto";
            bodyStyle.paddingRight = 0;
          }, 500);
        });
      });
    });
  });
};

const smoothScroll = () => {
  var links = document.querySelectorAll('a[href^="#"]');
  if (!links.length) {
    return;
  }
  links.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      var targetId = this.getAttribute("href").substring(1);

      var targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth" });
      } else {
        window.scroll({ top: 0, left: 0, behavior: "smooth" });
      }
    });
  });
};

const scrollUp = () => {
  const scrollUpElement = document.querySelector(".scroll-up");
  if (scrollUpElement) {
    scrollUpElement.addEventListener("click", () => {
      window.scroll({ top: 0, left: 0, behavior: "smooth" });
    });

    window.addEventListener("scroll", () => {
      const scrollCount = window.scrollY;

      if (scrollCount < 300) {
        scrollUpElement.classList.remove("active");
      }
      if (scrollCount > 300) {
        scrollUpElement.classList.add("active");
      }
    });
  }
};

// open drawer
const handleOpen = (drawer, drawerShow) => {
  const drawerContainer = drawer.parentNode;
  drawerShow.addEventListener("click", () => {
    const mobileControllerIcon = drawerShow.querySelector(".utilize-toggle");

    if (mobileControllerIcon) {
      mobileControllerIcon.classList.toggle("close");
    }
    drawerContainer.classList.add("active");
  });
};
// close drawer
const handleClose = (drawer, drawerShow, closedrawer) => {
  const drawerContainer = drawer.parentNode;
  closedrawer.addEventListener("click", () => {
    drawerContainer.classList.remove("active");
    const mobileControllerIcon = drawerShow.querySelector(".utilize-toggle");
    if (mobileControllerIcon) {
      mobileControllerIcon.classList.toggle("close");
    }
  });
};
// controll mobile menu
const drawer = () => {
  const drawerShowButtons = document.querySelectorAll(".show-drawer");
  const drawers = document.querySelectorAll(".drawer");
  if (drawerShowButtons?.length) {
    drawerShowButtons.forEach((drawerShow, idx) => {
      const drawer = drawers[idx];
      if (drawer) {
        const darawerContainer = drawer.parentNode;
        handleOpen(drawer, drawerShow);
        const closedrawers = darawerContainer.querySelectorAll(".close-drawer");
        closedrawers?.forEach((closedrawer) => {
          handleClose(drawer, drawerShow, closedrawer);
        });
      }
    });
  }
};

// style controllers

const controllerStyle = (accordionController, isActive) => {
  const rotateAbleLine = accordionController.querySelectorAll("span")[1];

  if (rotateAbleLine) {
    rotateAbleLine.style.transform = !isActive
      ? "rotate(0deg)"
      : "rotate(90deg)";
  }
};

// accordion hide and show
const toggleAccordion = (accordion, isActive, currentIndex, index) => {
  const parentContent = accordion.closest(".accordion-content");
  const content = accordion.querySelector(".accordion-content");
  const contentWrapper = accordion.querySelector(".content-wrapper");
  const contentHeight = contentWrapper.offsetHeight;

  let contenStyleHeight = content.style.height;
  if (contenStyleHeight === "auto") {
    content.style.height = `${contentHeight}px`;
  }

  setTimeout(() => {
    content.style.height = !isActive ? `${contentHeight}px` : 0;
  }, 1);
  if (!isActive) {
    setTimeout(() => {
      if (!parentContent) {
        content.style.height = `auto`;
      }
    }, 500);
  }
};

// get accordion controller and listen click event
const accordionController = (accordionContainer) => {
  const groupOfAccordion = accordionContainer.querySelectorAll(".accordion");

  groupOfAccordion.forEach((accordion, idx) => {
    const accordionController = accordion.querySelector(
      ".accordion-controller"
    );
    const isInitialyActive = accordion.classList.contains("active");

    if (isInitialyActive) {
      const contents = accordion.querySelector(".accordion-content");
      const contentHeight = contents.children[0].offsetHeight;
      if (contentHeight) {
        contents.style.height = `${contentHeight}px`;
      }
    }

    if (accordionController) {
      accordionController.addEventListener("click", function () {
        const currentAccordion = this.closest(".accordion");

        const isActive = currentAccordion.classList.contains("active");
        let waitForDblClick = setTimeout(() => {
          groupOfAccordion.forEach((accordion, idx1) => {
            const isAccordionController = accordion.querySelector(
              ".accordion-controller"
            );

            if (isAccordionController) {
              accordion.classList.remove("active");
              const accordionController = accordion.querySelector(
                ".accordion-controller"
              );
              controllerStyle(accordionController, true);
              toggleAccordion(accordion, true, idx, idx1);
            }
          });
          if (!isActive) {
            currentAccordion.classList.add("active");
            controllerStyle(accordionController, false);
            toggleAccordion(currentAccordion, false);
          }
        }, 10);
        accordionController.addEventListener("dblclick", function () {
          clearTimeout(waitForDblClick);
        });
      });
    }
  });
};
const accordions = () => {
  const accordionContainers = document.querySelectorAll(".accordion-container");

  if (!accordionContainers.length) {
    return;
  }
  accordionContainers.forEach((accordionContainer) => {
    accordionController(accordionContainer);
  });
};

const service = () => {
  const serviceCards = document.querySelectorAll(".service-cards");
  if (serviceCards?.length) {
    serviceCards.forEach((serviceCardsSingle) => {
      const allServiceCards =
        serviceCardsSingle.querySelectorAll(".service-card");

      allServiceCards.forEach((serviceCard, idx) => {
        serviceCard.addEventListener("mouseenter", function () {
          allServiceCards.forEach((serviceCard) => {
            serviceCard.classList.remove("active");
          });

          this.classList.add("active");
        });
      });
    });
  }
};

const stickystickyHeader = () => {
  const header = document.querySelector("header");
  const stickyHeader = header?.querySelector(".sticky-header");

  if (stickyHeader) {
    window.addEventListener("scroll", () => {
      const stickyHeaderHeight = stickyHeader.offsetHeight;
      const scrollCount = window.scrollY;

      // if (scrollCount - headerHeight < 0 && scrollCount - headerHeight > -5) {

      // }
      if (scrollCount < 300) {
        if (scrollCount > 200) {
          stickyHeader.setAttribute(
            "style",
            `position: fixed;top: -${stickyHeaderHeight}px;left:0;right:0
        `
          );
          stickyHeader.classList.remove("active");
        } else {
          stickyHeader.removeAttribute("style");
          stickyHeader.classList.remove("active");
        }
      }
      if (scrollCount > 300) {
        stickyHeader.setAttribute(
          "style",
          " position: fixed;top: 0px; left:0;right:0 "
        );
        stickyHeader.classList.add("active");
      }
    });
  }
};

const selects = document.querySelectorAll(".selectize");

if (selects?.length) {
  
  selects.forEach((select) => NiceSelect.bind(select));
}

drawer()
smoothScroll()
slider()
modal()
scrollUp()
accordions()
service()
stickystickyHeader()
