$(document).ready(function () {
  // $('a.external').attr('target', '_blank');
  $('a.external')
    .filter(
      (_, { href, hash }) =>
        !href.includes(location.href.split('#', 1)[0]) || !hash
    )
    .map((_, element) => {
      element.setAttribute('target', '_blank');
      element.setAttribute('rel', 'noopener noreferrer');
    });
});
