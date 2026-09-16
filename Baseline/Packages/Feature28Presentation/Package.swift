// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature28Presentation",
    products: [.library(name: "Feature28Presentation", targets: ["Feature28Presentation"])],
    dependencies: [.package(path: "../Feature28Domain"),
        .package(path: "../Feature28Data")],
    targets: [.target(name: "Feature28Presentation", dependencies: [.product(name: "Feature28Domain", package: "Feature28Domain"), .product(name: "Feature28Data", package: "Feature28Data")])]
)
