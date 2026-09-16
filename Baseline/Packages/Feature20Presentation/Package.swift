// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature20Presentation",
    products: [.library(name: "Feature20Presentation", targets: ["Feature20Presentation"])],
    dependencies: [.package(path: "../Feature20Domain"),
        .package(path: "../Feature20Data")],
    targets: [.target(name: "Feature20Presentation", dependencies: [.product(name: "Feature20Domain", package: "Feature20Domain"), .product(name: "Feature20Data", package: "Feature20Data")])]
)
