//Option 1 -- Sticky Navbar & Go Top
$(document).ready(function () {
  $(window).scroll(function () {
    if (this.scrollY > 100) {
      $(".navbar").addClass("sticky");
      $(".goTop").fadeIn();
    }
    else {
      $(".navbar").removeClass("sticky");
      $(".goTop").fadeOut();
    }
  });

  $(".goTop").click(function(){scroll(0,0)});

  $(".menu-toggler").click(function () {
    $(this).toggleClass("active");
    $(".navbar-menu").toggleClass("active");
  });

  // Հեռախոսով մենյուի կոճակներին սեղմելիս մենյուն փակվում է
  $(".menu-item").click(function () {
    $(".menu-toggler").removeClass("active");
    $(".navbar-menu").removeClass("active");
  });

});

//Option 2 -- Smooth Scroll
$('.navbar a').on('click', function (e) {
  if (this.hash !== '') {
    // Ստուգում ենք՝ արդյոք հիմա գտնվում ենք ԳԼԽԱՎՈՐ էջում
    if (window.location.pathname === '/' || window.location.pathname === '') {

      e.preventDefault(); // Արգելում ենք էջի թարմացումը ՄԻԱՅՆ գլխավոր էջում
      const hash = this.hash;

      // Համոզվում ենք, որ այդ բաժինը էջի վրա կա, նոր սքրոլ ենք անում
      if ($(hash).length) {
        $('html, body').animate(
          {
            scrollTop: $(hash).offset().top
          },
          1200
        );
      }
    }
    // Իսկ եթե գլխավոր էջում չենք, e.preventDefault() չի աշխատի,
    // և բրաուզերը կկատարի քո գրած հղումը՝ գնալով գլխավոր էջի համապատասխան բաժին:
  }
});

// About Text Appear Animation
window.addEventListener('scroll', function() {
    var aboutText = document.querySelector('.about-text');

    // Ստուգում ենք, որ էլեմենտը գոյություն ունենա, որպեսզի ուրիշ էջերում խնդիր չտա
    if (aboutText) {
      var position = aboutText.getBoundingClientRect().top;
      var screenPosition = window.innerHeight / 1.3;

      // Երբ հասնում ենք About բաժնին, ավելացնում ենք երևալու կլասը
      if(position < screenPosition) {
        aboutText.classList.add('about-text-appear');
      }
    }
});

// Մի հատ էլ միանգամից ստուգենք, գուցե էջը բացելիս արդեն About-ի վրա է
window.dispatchEvent(new Event('scroll'));

$(document).ready(function(){
    // 1. Dropdown-ը բացել/փակել առանց մենյուն փակելու
    $('.dropdown > a').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation(); // Սա ամենակարևորն է՝ կանխում է սեղմումը վերև անցնելուց

        $(this).next('.dropdown-content').toggleClass('show');
    });

    // 2. Մենյուն փակել միայն այն դեպքում, երբ սեղմում ենք ոչ-դրոփդաուն լինկերի վրա
    // Սելեկտորը ասում է՝ "բոլոր a-երը, բացի դրոփդաունը բացողից"
    $('.navbar-menu a:not(.dropdown > a)').on('click', function() {
        $('.navbar-menu').removeClass('active');
        $('.menu-toggler').removeClass('active');
        $('.dropdown-content').removeClass('show');
    });

    // 3. Եթե սեղմում ենք էկրանի ցանկացած այլ տեղ, փակել դրոփդաունը
    $(document).on('click', function() {
        $('.dropdown-content').removeClass('show');
    });
});

// Ընտրում ենք Footer-ը
  const footer = document.querySelector('footer');

  // Ստեղծում ենք դիտորդ (Observer), որը հասկանում է՝ երբ է Footer-ը երևում
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Երբ Footer-ը երևաց, ավելացնում ենք .active դասը
        footer.classList.add('active');
        // Կարող ենք նաև դադարեցնել դիտումը, որ անիմացիան չկրկնվի
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1 // Երբ footer-ի գոնե 10%-ը երևաց, անիմացիան կաշխատի
  });

  // Սկսում ենք հետևել Footer-ին
  observer.observe(footer);

  document.addEventListener('DOMContentLoaded', () => {
    const statsSection = document.querySelector('#stats');
    const counters = document.querySelectorAll('.counter');

    if (!statsSection) return; // Եթե չկա, ոչինչ չի անում

    const runCounter = () => {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const updateCounter = () => {
                const c = +counter.innerText;
                const increment = target / 100;
                if (c < target) {
                    counter.innerText = `${Math.ceil(c + increment)}`;
                    setTimeout(updateCounter, 20);
                } else {
                    counter.innerText = target;
                }
            };
            updateCounter();
        });
    };

    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            runCounter();
            observer.disconnect();
        }
    }, { threshold: 0.5 });

    observer.observe(statsSection);
});