import Feature28Domain
import Feature28Data

public enum Feature28PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature28DomainModel = Feature28DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
